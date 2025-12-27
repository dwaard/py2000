from context.Occurance import Occurance
from context.Song import Song

class EditionProcessor():
    """
    One Object can handle only One Edition Once
    """
    
    direct_match_count = 0
    songs_from_edition_count = 0
    similarity_match_count = 0
    new_songs_from_similarity_matrix = 0
    matches_from_similarity_matrix = 0
    
    def __init__(self, edition_reader=[], existing_data=[]
                , min_certain_ratio=0.9, min_relevant_ratio=0.6):
        self.new_song_list = []
        self.matched_song_occurance_tuple_list = []
        self.problem_tuple_list = []
        self.smtrx = {}
        self.min_certain_ratio = min_certain_ratio
        self.min_relevant_ratio = min_relevant_ratio
        self.year = edition_reader.edition
        self.picklist = [song for song in existing_data] # list of keys that ar not yet matched in this edition
        self.edition_dict = {}
        self.edition_data = [Occurance(row) for row in edition_reader]
        print("{} liedjes in de editie".format(len(self.edition_data)))
        

    def register_as_problem(self, problem_tuple):
        """
        Registers an occurance as a new song
        """
        self.problem_tuple_list.append(problem_tuple)

        
    def register_as_new_song(self, occurance):
        """
        Registers an occurance as a new song
        """
        self.new_song_list.append(Song(occurance))

        
    def register_as_match(self, song, occurance):
        """
        Registers an occurance as a match to a song
        """
        if song in self.picklist:
            self.picklist.remove(song)
        else:
            print("{} not in picklist".format(song))
        self.matched_song_occurance_tuple_list.append((song, occurance))
    
    def process_new_songs(self):
        """
        Adds all occurances as new songs if the year of the song is equal to the edition's year
        """
        self.songs_from_edition_count = 0
        remaining_edition_data = []
        for occ in self.edition_data:
            if occ.is_from_year(self.year):
                self.register_as_new_song(occ)                
                self.songs_from_edition_count+=1
            else:
                remaining_edition_data.append(occ)
        self.edition_data = remaining_edition_data
        print("{:5d} liedjes die in {} zijn uitgebracht".format(self.songs_from_edition_count, self.year))
        
    
    def print_multiple_matches(self, occ, matches):
        print("Ik heb een liedje met meer dan één match gevonden voor {}".format(occ))
        for m in matches:
            print(m)
    
    def process_exact_matches(self):
        """
        moves rows from edition_data only if the hash of the row exactly matches a key in the t2000_data
        """
        self.direct_match_count = 0
        remaining_edition_data = []
        for occ in self.edition_data:
            exact_matches = []
            for song in self.picklist:
                if song.is_exact_match(occ):
                    exact_matches.append(song)
            if len(exact_matches) > 0:
                if len(exact_matches) > 1:
                    self.print_multiple_matches(occ, exact_matches)
                else: # is exact 1
                    self.register_as_match(exact_matches[0], occ)
                    self.direct_match_count += 1
            else:
                remaining_edition_data.append(occ)
        self.edition_data = remaining_edition_data        
        print("{:5d} liedjes exact gematched".format(self.direct_match_count))
                
    
    def find_song_from_picklist_by_key(self, key):
        """
        Finds and returns the first song from the picklist where the specified key exactly matches one of its keys. 
        Otherwise it returns None
        """
        for song in self.picklist:
            if song.has_key(key):
                return song
        return None
    
    def process_manual_matches(self, match_dict={}):
        """
        Adds occurances to songs using the specified dictionary: { occurance_key : song_key }
        """
        self.manual_match_count = 0
        remaining_edition_data = []
        for occ in self.edition_data:
            if occ.key in match_dict:
                song = self.find_song_from_picklist_by_key(match_dict[occ.key])
                self.register_as_match(song, occ)
                self.manual_match_count += 1
            else:
                remaining_edition_data.append(occ)
        self.edition_data = remaining_edition_data
        print("{:5d} liedjes handmatig gematched".format(self.manual_match_count))
        
    
    def build_similarity_matrix(self):
        """
        Builds the similarity matrix: {occ : { ratio : song}}
        """
        print("Building similarity matrix...")
        remaining_edition_data = []
        self.smtrx = {}
        for occ in self.edition_data:
            data = {}
            for song in self.picklist:
                ratio = song.get_best_match(occ)
                if ratio >= self.min_relevant_ratio:
                    data[ratio] = song
            if len(data) > 0:
                self.smtrx[occ] = data
            else: # occurance cannot be matched, so add to remaining data
                remaining_edition_data.append(occ)
        self.edition_data = remaining_edition_data
        print("Done")
                

    def pop_largest_similarity(self):
        """
        Pops a tuple: (song, occurance, ratio) of the best possible match currently available in the similarity matrix
        and returns it. 
        If no match is found, because the similarity matrix is empty, it returns None. 
        When an occurance has no candidate song matches it returns a tuple (None, occurance, -1)
        """
        if len(self.smtrx)==0: # return None is matrix is empty
            return None
        
        best_ratio = -1
        best_occ = None
        best_song = None
        # find the highest ratio, occurance and song
        for occ, songs in self.smtrx.items():
            if len(songs)==0 and best_occ is None: # if we haven't found a bast yet and we encounter an empty dict
                best_occ = occ
            for ratio, song in songs.items():
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_occ = occ
                    best_song = song

        # remove the found occurance from the similarity matrix
        del self.smtrx[best_occ]
        
        if best_song is not None:
            # remove the found song from all dicts in the similarity matrix
            for songs in self.smtrx.values():
                # Using dictionary comprehension to find list 
                delete = [key for key in songs if songs[key] == best_song]
                for key in delete: del songs[key]            

        return (best_song, best_occ, best_ratio)
        
        
    def process_near_matches(self):
        """
        Processes the tuples in the similarity matrix. It either adds the tuple as a match, a problem (pending on the
        min_certain_ratio) or a new song (if pop_largest_similarity returns (None, occurance, -1)).
        """
        self.build_similarity_matrix()
        self.matches_from_similarity_matrix = 0
        while True:
            # match_tuple is: (occurance, song, similarity)
            match_tuple = self.pop_largest_similarity()

            if match_tuple is None: break # break the loop if there was nothin to pop left
            
            if match_tuple[0] is None: # if there was no song to match
                self.register_as_new_song(match_tuple[1])
            elif match_tuple[2] < self.min_certain_ratio: # if the ratio was lower than the minimum relevant threshold
                self.register_as_problem(match_tuple)
            else:
                self.register_as_match(match_tuple[0], match_tuple[1])
                self.matches_from_similarity_matrix += 1
        print("{:5d} liedjes gematched vanuit de similarity matrix".format(self.matches_from_similarity_matrix))
                
        
    def process_rest_as_new(self):
        """
        Processes the remander of edition_data as new songs
        """
        count = 0
        for occ in self.edition_data:
            self.register_as_new_song(occ)
            count+=1
        self.edition_data = []
        print("{:5d} liedjes niet gematched dus als nieuw toegevoegd".format(count))
            
            
    def has_problems(self):
        """
        Returns True if the processor has problems registered that avoid a correct merge
        """
        return len(self.problem_tuple_list) > 0
    
    
    def merge(self, existing_data):
        """
        Merges the imported data into the specified existing data
        """
        # add new songs
        for new in self.new_song_list:
            existing_data.append(new)
        
        # update matches
        for song, occ in self.matched_song_occurance_tuple_list:
            song.add_occurance(occ)

        return existing_data
    
    
    def print_status(self):
        pl = len(self.picklist)
        ed = len(self.edition_data)
        nw = len(self.new_song_list)
        mt = len(self.matched_song_occurance_tuple_list)
        sx = len(self.smtrx)
        pb = len(self.problem_tuple_list)
        print("Edition_data: {:4d} + {:4d} + {:4d} + {:4d} + {:4d} = {:4d}".format(
            ed, nw, mt, sx, pb, ed+nw+mt+sx+pb))
        print("Picklist    : {:4d} + {:4d} = {:4d}".format(pl, mt, pl+mt))
        
        
    def print_problems(self):
        print()
        print("=== {} PROBLEEMGEVALLEN ===".format(len(self.problem_tuple_list)))
        for item in self.problem_tuple_list:
            print("    '{}' : '{}' #{}".format(item[1].key, item[0].key, item[2]))        
        