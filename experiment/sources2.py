import csv, codecs, xlrd
from utils import UnicodeReader


def read_all():
    for row in read_1999_2014():
        yield row
    for row in read_2015():
        yield row
    for row in read_2016():
        yield row


def read_1999_2014():
    filename = 'raw/lijsten_alle_jaren.csv'
    print "Reading %s..." % filename
    reader = UnicodeReader(open(filename, 'r'), encoding="windows-1252",
                           delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    first = True
    for row in reader:
        if first: # skip first line
            first = False
        else:     # map content to output rows for each edition
            title = row[0]
            artist = row[1]
            year = int(row[2])
            # process 16 years (1999 - 2014)
            for i in range(0, 16):
                edition = 1999 + i
                position = int(row[3 + i])
                if position != 0:
                    yield [title, artist, year, edition, position]


def read_2015():
    filename = 'raw/TOP-2000-2015.csv'
    print "Reading %s..." % filename
    reader = UnicodeReader(open(filename, 'r'), encoding="windows-1252",
                           delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    first = True
    for row in reader:
        if first: # skip first line
            first = False
        else:     # map content to output rows for each edition
            title = row[1]
            artist = row[2]
            year = int(row[3])
            position = int(row[0])
            yield [title, artist, year, 2015, position]


def read_2016():
    filename = 'raw/TOP-2000-2016.xls'
    print "Reading %s..." % filename
    workbook = xlrd.open_workbook(filename, encoding_override='cp1252')
    worksheet = workbook.sheet_by_index(0)
    for row in range(1, worksheet.nrows):
        yield [worksheet.cell(row, 1).value,
                worksheet.cell(row, 2).value,
                worksheet.cell(row, 3).value,
                2016,
                worksheet.cell(row, 0).value,]


