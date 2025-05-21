
# Column positions of staged data array
TITLE = 0
ARTIST = 1
YEAR = 2
EDITION = 3
POSITION = 4
DECADE = 5
SCORE = 6

def transform(data):
    validate(data)
    data = clean_artist_name(data)
    data = clean_song_title(data)
    return data


def clean_artist_name(row):
    return row


def clean_song_title(row):
    return row


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
