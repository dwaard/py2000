class Artist:
    """
    Handles all about one artist, including all its songs, key generation
    """
    
    def __init__(self, song):
        """
        Constructor 
        """
        self.songs = []
        self.keys = song.get_artist_keyset()
        self.add_song(song)

        
    def is_exact_match(self, song):
        """
        returns True is one of the keys is an exact match of one of the the song's artist_keyset entries
        """
        for k in song.get_artist_keyset():
            if self.has_key(k):
                return True
        return False
        
        
    def has_key(self, key):
        """
        returns True is one of the keys is an exact match of the specified key
        """
        return key in self.keys
        
        
    def add_song(self, song):
        """
        Adds a song to this artist
        """
        self.songs.append(song)
        self.name = song.artist
        for k in song.get_artist_keyset():
            self.keys.add(k)
    
    def __repr__(self):
        return "{} ({} liedjes)".format(self.name, len(self.songs))