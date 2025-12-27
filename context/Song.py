import Levenshtein
from context.Occurance import Occurance

class Song:
    """
    Handles all about one song, including all its T2k occurances, key generation
    """
    
    def __init__(self, raw_data=None, cache_data=None):
        """
        Constructor
        """
        self.occurances = []
        self.keys = []
        if raw_data is not None:
            self.add_occurance(raw_data)
        else:
            if cache_data is not None:
                self.key = cache_data["key"]
                self.title = str(cache_data["title"])
                self.artist = cache_data["artist"]
                self.year = cache_data["year"]
                self.keys = cache_data["keys"]
                for occ_data in cache_data["occurances"]:
                    occ = Occurance(cache_data = occ_data)
                    self.occurances.append(occ)


        
    def is_exact_match(self, occurance):
        """
        returns True is one of the keys is an exact match of the occurance's key
        """
        return self.has_key(occurance.key)
        
        
    def has_key(self, key):
        """
        returns True is one of the keys is an exact match of the specified key
        """
        return key in self.keys
        
        
    def add_occurance(self, raw_data):
        """
        Adds an occurance to this song
        """
        self.occurances.append(raw_data)
        if raw_data.key not in self.keys:
            self.keys.append(raw_data.key)
        self.key = raw_data.key
        self.title = str(raw_data.data[Occurance.TITLE_INDEX])
        self.artist = raw_data.data[Occurance.ARTIST_INDEX]
        if raw_data.data[Occurance.YEAR_INDEX] is not None: 
            # remember previous year if year is not filled in
            self.year = raw_data.data[Occurance.YEAR_INDEX]
    
    
    def get_best_match(self, raw_data):
        best = 0
        for occ in self.occurances:
            ratio = Levenshtein.ratio(raw_data.key, occ.key)
            if ratio > best:
                best = ratio
        return best
        
        
    def get_best_key(self):
        """
        Returns the best available key from the occurances
        """
        return self.key
    
    def get_artist_keyset(self):
        result = []
        for occ in self.occurances:
            result.append(occ.artist_key)
        return set(result)
        

    def __repr__(self):
        return "{} - {} ({})".format(self.artist, self.title, self.year)

    def to_dict(self):
        return {
            "key": self.key,
            "title": self.title, 
            "artist": self.artist, 
            "year": self.year,
            "language": getattr(self, 'language', None),
            "en_title": getattr(self, 'en_title', None),
            "occurances": [occ.to_dict() for occ in self.occurances],
            "keys": self.keys
        }