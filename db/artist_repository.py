from repository import Repository

class ArtistRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Artist",
            [
                ('name', 'TEXT NOT NULL'),
            ])
        self.__cache = dict()

    def get_id(self, name, should_insert=True):
        if self._exists(name):
            return self.__cache[name]
        if not should_insert:
            return None
        self.append(name)
        return self.__cache[name]


    def _exists(self, name):
        return name in self.__cache

    def append(self, name):
        rowid = self._insert_row([name])
        self.__cache[name] = rowid
