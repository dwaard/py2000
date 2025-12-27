from context.storage.Repository import Repository


class SongRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Song",
            [
                ('artist', 'INTEGER NOT NULL'),
                ('title', 'TEXT NOT NULL'),
                ('year', 'INTEGER NOT NULL'),
                ('language', 'TEXT'),
                ('en_title', 'TEXT'),
            ])

    def append(self, artist_id, song_title, song_year, language, en_title):
        rowid = self._insert_row([artist_id, song_title, song_year, language, en_title])
        return rowid
