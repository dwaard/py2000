#
from datetime import datetime

from sources import *
from staging import StagedData


def extract():
    a = datetime.now()
    # Do stuff here
    print "Start extracting raw data into staged environment"
    s = StagedData()
    #s.clean()
    extract_1999_2014(s)
    extract_2015(s)
    extract_2016(s)
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished extracting in %.3f seconds" % delta


# Extracting the 1999-2014 csv
#
def extract_1999_2014(s):
    src = RawLijstenAlleJarenSource()
    row_count = src.row_count()
    print "Extracting: %s with %d rows" % (src.filename, row_count)
    for row in src:
        src.test(row) #validate content of row
        #map content to output rows for each edition
        title = row[0]
        artist = row[1]
        year = int(row[2])
        # process 16 years (1999 - 2014)
        for i in range(0, 16):
            edition = 1999 + i
            position = int(row[3 + i])
            if position != 0:
                s.append(title, artist, year, edition, position)


# Extracting the 2015 csv
#
def extract_2015(s):
    src = Raw2015Source()
    row_count = src.row_count()
    print "Extracting: %s with %d rows" % (src.filename, row_count)
    edition = 2015
    for row in src:
        src.test(row) #validate content of row
        #map content to output rows for each edition
        title = row[1]
        artist = row[2]
        year = int(row[3])
        position = int(row[0])
        s.append(title, artist, year, edition, position)



def extract_2016(s):
    src = Raw2016Source()
    row_count = src.row_count()
    print "Extracting: %s with %d rows" % (src.filename, row_count)
    edition = 2016
    for row in src:
        src.test(row) #validate content of row
        #map content to output rows for each edition
        title = row[1]
        artist = row[2]
        year = int(row[3])
        position = int(row[0])
        s.append(title, artist, year, edition, position)

extract()