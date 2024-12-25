from db.repository import Repository

class ArtistRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Artist",
            [
                ('name', 'TEXT NOT NULL'),
            ]
        )

    def append(self, name):
        rowid = self._insert_row([name])
        return rowid
