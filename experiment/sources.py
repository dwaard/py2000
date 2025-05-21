import csv, codecs, xlrd
from utils import UnicodeReader

class RawLijstenAlleJarenSource():

    def __init__(self):
        self.filename = 'raw/lijsten_alle_jaren.csv'

    def row_count(self):
        return len(open(self.filename).readlines()) - 1 # header row

    def test(self, row):
        if len(row)!=19:
            raise ValueError("Row %s has not 19 but %d columns." % (repr(row), len(row)))
        if not row[2].isdigit():
            raise ValueError("Row %s has no valid year in third column: %s" % (repr(row), row[2]))
        year = int(row[2])
        if year<1800 or year>2999:
            raise ValueError("Row %s has no valid year in third column: %s" % (repr(row), row[2]))
        for i in range(0,16):
            edition = 1999 + i
            position = int(row[3 + i])
            if position<0 or position > 2000:
                raise ValueError("Row %s has no valid position (%i) for edition %i" % (repr(row), position, edition))


    def __iter__(self):
        self.reader = UnicodeReader(open(self.filename, 'r'), encoding="windows-1252",
                                       delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.count = 0
        return self


    def next(self):
        n = self.reader.next()
        if self.count==0: # skip header line
            n = self.reader.next()
        self.count = self.count+1
        return n;



class Raw2015Source():
    def __init__(self):
        self.filename = 'raw/TOP-2000-2015.csv'

    def row_count(self):
        return len(open(self.filename).readlines()) - 1 # header row

    def test(self, row):
        if len(row)!=4:
            raise ValueError("Row %s has not 19 but %d columns." % (repr(row), len(row)))
        if not row[0].isdigit():
            raise ValueError("Row %s has no number in first column: %s" % (repr(row), row[0]))
        position = int(row[0])
        if position < 0 or position > 2000:
            raise ValueError("Row %s has no valid position (%i)" % (repr(row), position))
        if not row[3].isdigit():
            raise ValueError("Row %s has no number in fourth column: %s" % (repr(row), row[3]))
        year = int(row[3])
        if year<1800 or year>2999:
            raise ValueError("Row %s has no valid year in fourth column: %s" % (repr(row), row[3]))


    def __iter__(self):
        self.reader = UnicodeReader(open(self.filename, 'r'), encoding="windows-1252",
                                       delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.count = 0
        return self


    def next(self):
        n = self.reader.next()
        if self.count==0: # skip header line
            n = self.reader.next()
        self.count = self.count+1
        return n;


class Raw2016Source():
    def __init__(self):
        self.filename = 'raw/TOP-2000-2016.xls'

    def row_count(self):
        return 2000

    def test(self, row):
        if len(row) != 4:
            raise ValueError("Row %s has not 19 but %d columns." % (repr(row), len(row)))
        position = int(row[0])
        if position <= 0 or position > 2000:
            raise ValueError("Row %s has no valid position (%i)" % (repr(row), position))
        year = int(row[3])
        if year < 1800 or year > 2999:
            raise ValueError("Row %s has no valid year in fourth column: %s" % (repr(row), row[3]))

    def __iter__(self):
        self.workbook = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        self.worksheet = self.workbook.sheet_by_index(0)
        self.count = 0
        return self

    def next(self):
        self.count = self.count+1
        if self.count > 2000:
            raise StopIteration
        return [self.worksheet.cell(self.count, 0).value,
                self.worksheet.cell(self.count, 1).value,
                self.worksheet.cell(self.count, 2).value,
                self.worksheet.cell(self.count, 3).value,]


# s = Raw2016Source()
# for row in s:
#     s.test(row)
#     print repr(row)
