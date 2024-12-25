import csv

class LijstenAlleJarenReader:
    filename = 'raw/lijsten_alle_jaren.csv'
    base = 1999 # year of first edition
    index = 0  # number of editions

    def __init__(self):
        print ("Reading %s..." % self.filename)
        self.reader = csv.reader(open(self.filename, 'r', encoding="latin1"),
                               delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.first: # skip first row
            self.row = next(self.reader)
            self.row = next(self.reader)
            self.first = False
        if self.index > 15: # read next line when needed
            self.index = 0
            self.row = next(self.reader)
        title = self.row[0]
        artist = self.row[1]
        year = int(self.row[2])
        edition = self.base + self.index
        position = int(self.row[3 + self.index])
        self.index += 1
        return [title, artist, year, edition, position]
