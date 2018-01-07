import csv

from experiment.utils import UnicodeReader


class LijstenAlleJarenReader:
    filename = 'raw/lijsten_alle_jaren.csv'
    base = 1999 # year of first edition
    index = 0  # number of editions

    def __init__(self):
        print "Reading %s..." % self.filename
        self.reader = UnicodeReader(open(self.filename, 'r'), encoding="windows-1252",
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.first = True

    def __iter__(self):
        return self

    def next(self):
        if self.first: # skip first row
            self.row = self.reader.next()
            self.row = self.reader.next()
            self.first = False
        if self.index > 15: # read next line when needed
            self.index = 0
            self.row = self.reader.next()
        title = self.row[0]
        artist = self.row[1]
        year = int(self.row[2])
        edition = self.base + self.index
        position = int(self.row[3 + self.index])
        self.index += 1
        return [title, artist, year, edition, position]

    def rows(self):
        print "Reading %s..." % self.filename
        reader = UnicodeReader(open(self.filename, 'r'), encoding="windows-1252",
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        first = True
        for row in reader:
            if first:  # skip first line
                first = False
            else:  # map content to output rows for each edition
                title = row[0]
                artist = row[1]
                year = int(row[2])
                # process 16 years (1999 - 2014)
                for i in range(0, 16):
                    edition = 1999 + i
                    position = int(row[3 + i])
                    if position != 0:
                        yield [title, artist, year, edition, position]

