import csv

from utils import UnicodeReader


class CSVReader:

    def __init__(self, filename, edition):
        self.edition = edition
        print ("Reading %s..." % filename)
        self.reader = csv.reader(open(filename, 'r', encoding="latin1"),
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.first = True

    def __iter__(self):
        return self

    def __next__(self):
        row = self.reader.__next__()
        if self.first:
            row = self.reader.__next__()
            self.first = False
        title = row[1]
        artist = row[2]
        year = int(row[3])
        position = int(row[0])
        return [title, artist, year, self.edition, position]
