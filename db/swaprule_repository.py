from repository import Repository


class SwapruleRepository(Repository):
    """"
    Algemene regel:
    als title==null, dan geldt voor alle rijen van die artiest (year wordt genegeerd)
    als de 'new_' veld is gevuld, dan replacen
    """

    def __init__(self, conn):
        Repository.__init__(
            self,
            conn,
            "Swaprules",
            [
                ('artist', 'TEXT NOT NULL'),
                ('title', 'INTEGER'),
                ('year', 'INTEGER'),
                ('new_artist', 'TEXT'),
                ('new_title', 'INTEGER'),
                ('new_year', 'INTEGER'),
                ('count', 'INTEGER DEFAULT 0'),
            ])
        self.__cache = dict()

    def append(self, data):
        self._insert_row(data)
        self.commit()

    def rules_for_artist_only(self, name):
        if name not in self.__cache:
            self.__cache[name] = [rule for rule in self.read_all(where='artist=?', params=[name])]
        for rule in self.__cache[name]:
            yield rule

    def save_rule_counts(self):
        sql = 'UPDATE %s SET COUNT=? WHERE rowid=?' % self._table_name
        c = self.conn.cursor()
        # print self.__cache
        for ruleset in self.__cache.itervalues():
            for rule in ruleset:
                c.execute(sql, [int(rule['count']), int(rule['rowid'])])

    def reset_counts(self):
        sql = 'UPDATE %s SET count=0' % self._table_name
        c = self.conn.cursor()
        c.execute(sql)


