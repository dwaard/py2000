from LijstenAlleJarenReader import LijstenAlleJarenReader
from TT2015Reader import TT2015Reader
from TT2016Reader import TT2016Reader
from TT2017Reader import TT2017Reader

ARTIST_COLUMN = 1
TITLE_COLUMN = 0
SONG_YEAR_COLUMN = 2
EDITION_YEAR_COLUMN = 3
EDITION_POSITION_COLUMN = 4

'''
All readers should return an array with the following items:
 0 - Song title (String with len>0)
 1 - Artist name (String with len>0)
 2 - Release year of song (number from 1800 to current year)
 3 - Top2000 Edition from 1999 to ...
 4 - Position of the song in the edition (1...2000, 0 if song did not occur)
'''
def all_rows():
    for row in LijstenAlleJarenReader():
        # ignore iterations that return a zero position
        if row[4] != 0:
            yield row
    for row in TT2015Reader():
        yield row
    for row in TT2016Reader():
        yield row
    for row in TT2017Reader():
        yield row

def help():
    print 'Reader leest alle ruwe data'