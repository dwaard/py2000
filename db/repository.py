
class Repository:

    def __init__(self, conn, table_name, column_def):
        self.conn = conn
        self._table_name = table_name
        self._column_def = column_def
        self._column_count = len(column_def)
        self.create_table()

    def create_table(self):
        """"
        Creates the table according _table_name and _column_def if the tabel does not exist
        """
        c = self.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS %s (%s)" % (
            self._table_name,
            ", ".join("%s %s" % tup for tup in self._column_def)
        )
        c.execute(sql)

    def truncate(self):
        """" deletes all records from this table """
        c = self.conn.cursor()
        sql = "DELETE FROM %s;" % self._table_name
        c.execute(sql)

    def read_rowid(self, rowid, selection='rowid, *', order_by='1'):
        """" Executes a SELECT query for given rowid, and returns the first row as a dictionary """
        for row in self.read_sql_to_dict("SELECT %s FROM %s WHERE rowid=? ORDER BY %s" %
                                     (selection, self._table_name, order_by), [rowid]):
            return row

    def read_row(self, selection='rowid, *', where="1", order_by='1', params=[]):
        """" Executes a SELECT query, and returns the first row as a dictionary """
        for row in self.read_sql_to_dict("SELECT %s FROM %s WHERE %s ORDER BY %s" %
                                     (selection, self._table_name, where, order_by), params):
            return row

    def read_all(self, selection='rowid, *', where="1", order_by='1', params=[]):
        """" Executes a SELECT query, and yields each row as a dictionary """
        return self.read_sql_to_dict("SELECT %s FROM %s WHERE %s ORDER BY %s" %
                                     (selection, self._table_name, where, order_by), params)

    def read_sql_to_dict(self, sql, params=[]):
        """" Executes SQL query, and yields a dict for each row. The dict contains a key for each entry in names and
        a value from the row corresponding to the names index. the names and row are zipped. """
        c = self.conn.cursor()
        rs = c.execute(sql, params)
        names = [tuple[0] for tuple in rs.description]
        for row in c.execute(sql, params):
            yield {name: value for name, value in zip(names, row)}

    def read_one_row(self, sql, params):
        """" Executes a SELECT query and returns the first row as a dict """
        c = self.conn.cursor()
        c.execute(sql, params)
        row = c.fetchone()
        return row

    def _insert_row(self, iterable, ignore=False):
        """" Inserts rows of data in the database using the tablespec to genereate the query. If ignore=True the 
         query will be changed from INSERT into INSERT OR IGNORE"""
        sql = "INSERT %s INTO %s VALUES (%s)" % ("OR IGNORE" if ignore else "", self._table_name, ','
                                                 .join(['?' for _ in range(self._column_count)]))
        c = self.conn.cursor()
        c.execute(sql, iterable)
        return c.lastrowid

    def count(self, selection = '*', where='True', params=[]):
        sql = "SELECT COUNT(%s) FROM %s WHERE %s" % (selection, self._table_name, where)
        result = self.read_one_row(sql, params)
        return result[0]

    def commit(self):
        self.conn.commit()

    def insert_rows(self, iterable, ignore=False):
        """" Inserts rows of data in the database using the tablespec to genereate the query. If ignore=True the 
         query will be changed from INSERT into INSERT OR IGNORE"""
        sql = "INSERT %s INTO %s VALUES (%s)" % ("OR IGNORE" if ignore else "", self._table_name, ','
                                                 .join(['?' for _ in range(self._column_count)]))
        c = self.conn.cursor()
        c.executemany(sql, iterable)
        self.conn.commit()
