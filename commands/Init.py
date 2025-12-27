import os, csv, json
import commands
from context.Occurance import Occurance
from context.Song import Song

class Init(commands.AbstractCommand):
    """
    Initializes the context with initial data (editions 1999-2014)
    """
    min_year = 1999 # year of the very first T2K edition
    max_year = 2014 # year of the last edition in this file
    min_index = 3  # first column to read from

    
    def print_help(self, context):
        print("Initializes the context with initial data (editions 1999-2014). It extracts all the raw data up to the latest year.")


    def execute(self, context):
        cache_exists = ("CACHED_DATA" in os.environ) and os.path.isfile(os.environ["CACHED_DATA"])

        if cache_exists:
            return self.init_from_cache(context)

        return self.init_from_scratch(context)


    def init_from_cache(self, context):
        print("Cache file found, loading data from cache...")
        with open(os.environ["CACHED_DATA"], "r") as infile:
            import json
            data = json.load(infile)
            songs = []
            for song_data in data:
                song = Song(cache_data = song_data)  # dummy occurance to create the song
                songs.append(song)
                max_year = max([occ.data[Occurance.EDITION_INDEX] for occ in song.occurances if occ.data[Occurance.EDITION_INDEX] is not None] + [self.min_year])
                if max_year > self.max_year:
                    self.max_year = max_year
            context.set_data(self.max_year, songs)
        print(f"Loaded {len(songs)} songs from cache.")
        return False       


    def init_from_scratch(self, context):
        print("Cache file NOT found, loading data from raw datafiles...")
        t2k_1999_2014_data = {} # dict that holds all Songs from 1999-2014 editions
        for row in self.read_rows():
            if row[4] != 0: # ignore iterations that return a zero position
                occ = Occurance(row)
                if not occ.key in t2k_1999_2014_data:
                    t2k_1999_2014_data[occ.key] = Song(occ)
                else:
                    t2k_1999_2014_data[occ.key].add_occurance(occ)
                
        # t2k_data holds all extracted data
        t2k_data = list(t2k_1999_2014_data.values())
        print(f"Read {len(t2k_data)} songs")
        context.set_data(self.max_year, t2k_data)

        # Save the context data to a json cache file
        with open(os.environ["CACHED_DATA"], "w") as outfile:
            json.dump([song.to_dict() for song in context.data], outfile, indent=2)        

        return False


    def read_rows(self):
        self.filename = os.environ["INITIAL_DATA_FILE"]
        print ("Reading %s..." % self.filename)
        self.reader = csv.reader(open(self.filename, 'r', encoding="latin1"),
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.first = True
        for row in self.reader:
            # Each line is a song with all occurrances. "0" when song did not occur then
            if self.first: # skip first row
                self.first = False
            else:
                max_index = self.min_index + self.max_year - self.min_year
                for index in range(self.min_index, max_index + 1):
                    # Loop tover all the occurance columns
                    title = row[0]
                    artist = row[1]
                    year = int(row[2])
                    edition = self.min_year + index - self.min_index
                    position = int(row[index])
                    yield [title, artist, year, edition, position]
