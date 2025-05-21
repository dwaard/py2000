from db.repository import Repository


class OccurrenceRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Occurance",
            [
                ('song', 'INTEGER NOT NULL'),
                ('title', 'TEXT NOT NULL'),
                ('artist', 'TEXT NOT NULL'),
                ('year', 'INTEGER NOT NULL'),
                ('edition', 'INTEGER NOT NULL'),
                ('position', 'INTEGER NOT NULL')
            ])


    def append(self, data):
        self._insert_row(data)