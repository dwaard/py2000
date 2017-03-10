import codecs
import csv
import xlrd
import xlwt

from utils import UnicodeReader

# Column positions of staged data array
TITLE = 0
ARTIST = 1
YEAR = 2
EDITION = 3
POSITION = 4
DECADE = 5
SCORE = 6


class SongFile:
    filename = "staged/song_cleaning.xls"
    swap_list = dict()
    ignore_list = dict()

    def __init__(self):
        self.data = []
        try:
            rd = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        except IOError:
            wt = xlwt.Workbook()
            wt.add_sheet('swap_list')
            wt.add_sheet('ignore_list')
            wt.add_sheet('raw_data')
            wt.save(self.filename)
            rd = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        # read the swap list
        ws = rd.sheet_by_name('swap_list')
        for row in range(ws.nrows):
            artist = ws.cell(row, 0).value
            current = ws.cell(row, 1).value
            changeto = ws.cell(row, 2).value
            current_name = "%s - %s" % (current, artist)
            self.swap_list[current_name] = changeto
        # read the swap list
        ws = rd.sheet_by_name('ignore_list')
        for row in range(ws.nrows):
            artist = ws.cell(row, 0).value
            current = ws.cell(row, 1).value
            changeto = ws.cell(row, 2).value
            current_name = "%s - %s" % (current, artist)
            self.ignore_list[current_name] = changeto

    def should_ignore_on_analyze(self, name1, name2):
        if not self.ignore_list.has_key(name1):
            return False
        return self.ignore_list[name1] == name2

    def clean_title(self, artist, title):
        title = title.strip()
        name = "%s - %s" % (title, artist)
        if self.swap_list.has_key(name):
            return self.swap_list[name]
        return title


class ArtistFile:
    filename = "staged/artist_cleaning.xls"
    swap_list = dict()
    ignore_list = dict()

    def __init__(self):
        self.data = []
        try:
            rd = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        except IOError:
            wt = xlwt.Workbook()
            wt.add_sheet('swap_list')
            wt.add_sheet('ignore_list')
            wt.add_sheet('raw_data')
            wt.save(self.filename)
            rd = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        # read the swap list
        ws = rd.sheet_by_name('swap_list')
        for row in range(ws.nrows):
            current = ws.cell(row, 0).value
            changeto = ws.cell(row, 1).value
            self.swap_list[current] = changeto
        # read the swap list
        ws = rd.sheet_by_name('ignore_list')
        for row in range(ws.nrows):
            current = ws.cell(row, 0).value
            changeto = ws.cell(row, 1).value
            self.ignore_list[current] = changeto

    def should_ignore_on_analyze(self, name1, name2):
        if not self.ignore_list.has_key(name1):
            return False
        return self.ignore_list[name1] == name2

    def clean(self, name):
        name = name.strip()
        if self.swap_list.has_key(name):
            return self.swap_list[name]
        return name


class StagedData:
    filename = "staged/data.csv"
    artist_file = ArtistFile()
    song_file = SongFile()

    def read_rows(self):
        reader = UnicodeReader(open(self.filename, 'r'), encoding="cp1252",
                               delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if not (len(row) == 7):
                raise ValueError("Invalid row %s" % row)
            yield([row[TITLE], row[ARTIST], int(row[YEAR]), int(row[EDITION]), int(row[POSITION])])

    def cache_analyze_data(self):
        result_dict = dict()
        for row in self.read_rows():
            # get existing artist_dict from dict or make new
            artist_dict = dict()
            if row[ARTIST] in result_dict:
                artist_dict = result_dict[row[ARTIST]]
            else:
                result_dict[row[ARTIST]] = artist_dict
            # get existing song_dict from artist_dict or make new
            song_dict = dict()
            if row[TITLE] in artist_dict:
                song_dict = artist_dict[row[TITLE]]
            else:
                song_dict['year'] = row[YEAR]
                artist_dict[row[TITLE]] = song_dict
            # in song_dict, set (edition, posisition)
            song_dict[row[EDITION]] = row[POSITION]
        return result_dict

    def writer(self):
        if not hasattr(self, '_writer'):
            self._writer = codecs.open(self.filename, encoding='cp1252', mode='w')
        return self._writer

    def append(self, data):
        validate(data)
        data[ARTIST] = self.artist_file.clean(data[ARTIST])
        data[TITLE] = self.song_file.clean_title(data[ARTIST], data[TITLE])
        data[YEAR] = clean_number(data[YEAR])
        data[EDITION] = clean_number(data[EDITION])
        data[POSITION] = clean_number(data[POSITION])
        line = '"%s";"%s";%d;%d;%d;"%d";%d\n' % (data[TITLE], data[ARTIST], data[YEAR], data[EDITION], data[POSITION], (data[YEAR]/10) * 10, 2001 - data[POSITION])
        self.writer().write(line)


def clean_number(float_or_int):
    return int(float_or_int)


def validate(row):
    # check number of columns
    if len(row)!=5:
        raise ValueError("Row %s has not 5 but %d columns." % (repr(row), len(row)))

    # check title
    if len(row[TITLE]) == 0:
        raise ValueError("Empty title in %s" % repr(row))

    # check artist
    if len(row[ARTIST]) == 0:
        raise ValueError("Empty artist in %s" % repr(row))

    # check year
    if not (isinstance(row[YEAR], int) or isinstance(row[YEAR], float)):
        raise ValueError("No number in year column: %s" % repr(row))
    year = int(row[YEAR])
    if year<1800 or year>2999:
        raise ValueError("No valid year column: %s" % repr(row))

    # check edition
    if not (isinstance(row[EDITION], int) or isinstance(row[EDITION], float)):
        raise ValueError("No number in edition column: %s" % repr(row))
    edition = int(row[EDITION])
    if edition<1999 or edition>2999:
        raise ValueError("No valid year column: %s" % repr(row))

    #check posistion
    if not (isinstance(row[POSITION], int) or isinstance(row[POSITION], float)):
        raise ValueError("No number in position column: %s" % repr(row))
    position = row[POSITION]
    if position < 0 or position > 2000:
        raise ValueError("Invalid position: %s" % repr(row))
