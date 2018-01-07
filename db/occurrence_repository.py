from repository import Repository


class OccurrenceRepository(Repository):

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Occurance",
            [
                ('song', 'INTEGER NOT NULL'),
                ('edition', 'INTEGER NOT NULL'),
                ('position', 'INTEGER NOT NULL')
            ])


    def append(self, data):
        self._insert_row(data)