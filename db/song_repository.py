from repository import Repository


class SongRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Song",
            [
                ('artist', 'INTEGER NOT NULL'),
                ('title', 'TEXT NOT NULL'),
                ('year', 'INTEGER NOT NULL')
            ])
        self.__cache = dict()

    def get_id(self, artist_id, song_title, song_year, should_insert=True):
        if not self.exists(artist_id, song_title):
            if not should_insert:
                return None
            self.append(artist_id, song_title, song_year)
        return self.__cache[(artist_id, song_title)]

    def exists(self, artist_id, song_title):
        return (artist_id, song_title) in self.__cache

    def append(self, artist_id, song_title, song_year):
        rowid = self._insert_row([artist_id, song_title, song_year])
        self.__cache[(artist_id, song_title)] = rowid
