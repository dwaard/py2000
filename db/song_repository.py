from db.repository import Repository


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

    def append(self, artist_id, song_title, song_year):
        rowid = self._insert_row([artist_id, song_title, song_year])
        return rowid
