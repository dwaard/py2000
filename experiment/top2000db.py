import sqlite3

# Column positions of staged data array
TITLE = 0
ARTIST = 1
YEAR = 2
EDITION = 3
POSITION = 4

class DB:
    conn = sqlite3.connect('data/datawarehouse.sqlite')

    def add_row(self, data):
        print "test"