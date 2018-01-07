from repository import Repository


class IgnoreruleRepository(Repository):
    """"
    Algemene regel:
    als title==null, dan geldt voor alle rijen van die artiest (year wordt genegeerd)
    als de 'new_' veld is gevuld, dan replacen
    """

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Ignorerules",
            [
                ('artist1', 'TEXT NOT NULL'),
                ('title1', 'TEXT'),
                ('artist2', 'TEXT'),
                ('title2', 'TEXT'),
            ])
        self.__init_cache()

    def __init_cache(self):
        self.__cache = dict()
        for rule in self.read_all(where='artist2 IS NOT NULL'):
            self.__cache[(rule['artist1'], rule['artist2'])] = True
        for rule in self.read_all(where='title1 IS NOT NULL AND title2 IS NOT NULL'):
            self.__cache[(rule['artist1'], rule['title1'], rule['title2'])] = True

    def append(self, data):
        self._insert_row(data)
        self.commit()

    def rulecount_for_artists(self, name1, name2):
        try:
            return self.__cache[(name1, name2)]
        except KeyError:
            return 0

    def rulecount_for_songs(self, artist, title1, title2):
        try:
            return self.__cache[(artist, title1, title2)]
        except KeyError:
            return 0
