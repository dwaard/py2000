import csv

from experiment.utils import UnicodeReader


class TT2015Reader:
    filename = 'raw/TOP-2000-2015.csv'

    def __init__(self):
        print "Reading %s..." % self.filename
        self.reader = UnicodeReader(open(self.filename, 'r'), encoding="windows-1252",
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.first = True

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        if self.first:
            row = self.reader.next()
            self.first = False
        title = row[1]
        artist = row[2]
        year = int(row[3])
        position = int(row[0])
        return [title, artist, year, 2015, position]

