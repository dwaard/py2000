import codecs
import csv

from artistfile import ArtistFile
from experiment.utils import UnicodeReader
from songfile import SongFile

# Column positions of staged data array
TITLE = 0
ARTIST = 1
YEAR = 2
EDITION = 3
POSITION = 4
DECADE = 5
SCORE = 6

EXPECTED_COLUMN_COUNT = 7
EXPECTED_RAW_COLUMN_COUNT = 5


class StagedData:
    """
    Deze klasse is een Repository naar de Staged data. 
    """

    filename = "staged/data.csv"

    FILE_ENCODING = 'UTF-8'

    artist_file = ArtistFile()

    song_file = SongFile()

    def read_rows(self):
        """
        Iterator die alle rijen afstaat uit het staged databestand.
        :return: van elke rij: [TITLE, ARTIST, YEAR, EDITION, POSITION]
        """
        reader = UnicodeReader(open(self.filename, 'r'), encoding=self.FILE_ENCODING,
                               delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if not (len(row) == EXPECTED_COLUMN_COUNT):
                raise ValueError("Row %s has not %d but %d columns." % (repr(row), EXPECTED_COLUMN_COUNT, len(row)))
            yield([row[TITLE], row[ARTIST], int(row[YEAR]), int(row[EDITION]), int(row[POSITION])])

    def cache_analyze_data(self):
        """
        Retourneert een dict met per ARTIST:
         een dict met daarin per TITLE:
          een dict met daarin achter 'year' het YEAR van de song, en per EDITION de POSITION  
        :return: 
        """
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
        """"
        Retourneert het _writer attribuut
        """
        if not hasattr(self, '_writer'):
            self._writer = codecs.open(self.filename, encoding=self.FILE_ENCODING, mode='w')
        return self._writer

    def append(self, data):
        """"
        Voegt een nieuwe regel toe aan het databestand, als de data valide is
        """
        validate(data)
        # data[ARTIST] = self.artist_file.clean(data[ARTIST])
        # data[TITLE] = self.song_file.clean_title(data[ARTIST], data[TITLE])
        # data[YEAR] = clean_number(data[YEAR])
        # data[EDITION] = clean_number(data[EDITION])
        # data[POSITION] = clean_number(data[POSITION])
        line = '"%s";"%s";%d;%d;%d\n' % (data[TITLE], data[ARTIST], data[YEAR], data[EDITION], data[POSITION])
        # line = '"%s";"%s";%d;%d;%d;"%d";%d\n' % (data[TITLE], data[ARTIST], data[YEAR], data[EDITION], data[POSITION], (data[YEAR]/10) * 10, 2001 - data[POSITION])
        self.writer().write(line)


def clean_number(float_or_int):
    """"
    Maakt van een onzeker getalformaat een int.
    """
    return int(float_or_int)


def validate(row):
    """"
    Controleert of de inhoud van row voldoet aan de validatieregels.
    """
    # check number of columns
    if len(row) != EXPECTED_RAW_COLUMN_COUNT:
        raise ValueError("Row %s has not %d but %d columns." % (repr(row), EXPECTED_RAW_COLUMN_COUNT, len(row)))

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
