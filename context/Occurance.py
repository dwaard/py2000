

class Occurance:
    """
    Represents exactly one row from one T2k edition
    """
    TITLE_INDEX = 0
    ARTIST_INDEX = 1
    YEAR_INDEX = 2
    EDITION_INDEX = 3
    POSITION_INDEX = 4
    
    
    def __init__(self, raw_data=None, cache_data=None):
        if raw_data is not None:
            if len(raw_data[self.ARTIST_INDEX]) == 0:
                raise ValueError("Trying to add an empty row")
            self.data = raw_data
            self.key = self.__generate_key__(raw_data)
            self.artist_key = self.__normasize__(raw_data[self.ARTIST_INDEX])
            self.edition = raw_data[self.EDITION_INDEX]
            self.position = raw_data[self.POSITION_INDEX]
        elif cache_data is not None:
            self.data = cache_data["data"]
            self.key = cache_data["key"]
            self.artist_key = cache_data["artist_key"]
            self.edition = cache_data["edition"]
            self.position = cache_data["position"]
        else:
            raise ValueError("Either row or cache_data must be provided")

    def is_from_year(self, year):
        """
        Returns True if and only if we are sure that this song is published in the given year
        """
        return self.data[self.YEAR_INDEX] is not None and self.data[self.YEAR_INDEX]==year
    
    
    def __generate_key__(self, raw_data):
        """
        Returns a string representing the normasized title and artist
        """
        return self.__normasize__(raw_data[self.TITLE_INDEX], raw_data[self.ARTIST_INDEX])
    
    def __normasize__(self, *args):
        """
        Returns a string representing a normalized text specific for song titles and artist names.
        """
        # first, join all arguments into one single string, where all None args are removed
        s = " ".join([str(s) for s in list(args) if s is not None])
        s = s.lower() # change to lower case
        if s.startswith("the "): # remove leading the
            s = s[4:]
        if s.startswith("de "): # remove leading de
            s = s[3:]
        if s.startswith("les "): # remove leading de
            s = s[4:]
        # remove some other standard words
        s = (s.replace("/", " ") 
                .replace("-", " ")
                .replace("'", "")
                .replace(".", "")
                .replace(",", "")
                .replace("!", "")
                .replace("?", "")
                .replace("(", "")
                .replace(")", "")
                .replace("ë", "e")
                .replace("ö", "o")
                .replace("å", "a")
                .replace("ø", "o")
                .replace(" the ", " ") # should handle artist 'the the' nicely
                .replace(" de ", " ")
                .replace(" and ", " ")
                .replace(" en ", " ")
                .replace(" & ", " ")
                .replace(" feat", "")
                .replace(" ft", "")
                .replace("\xa0", " ")
                .replace("\ufeff", "")
                .replace(" albumversie ", " ")
        )
        while "  " in s: # remove all extra spaces
            s = s.replace("  ", " ")
        s = s.strip() # remove all leading and trailing spaces
        return s
    
    def __repr__(self):
        return "{} - {} ({}): {}".format(
            self.data[self.ARTIST_INDEX], self.data[self.TITLE_INDEX], self.data[self.YEAR_INDEX], 
            self.data[self.POSITION_INDEX])    

    def to_dict(self):
        return {
            "key": self.key,
            "artist_key": self.artist_key, 
            "edition": self.edition, 
            "position": self.position,
            "data": self.data
        }        
