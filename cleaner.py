import db
import reader

nonBreakSpace = u'\xa0'

def clean(data):
    """" Cleans artist, title and year for the song """
    data[reader.ARTIST_COLUMN] = clean_artist(data)
    data[reader.TITLE_COLUMN] = clean_title(data)
    data[reader.SONG_YEAR_COLUMN] = clean_year(data)
    return data


def clean_artist(data):
    result = data[reader.ARTIST_COLUMN].strip().replace(nonBreakSpace, " ")
    rule = get_rule_for_artist_only(result)
    while rule:
        result = rule['new_artist']
        rule['count'] += 1
        rule = get_rule_for_artist_only(result)
    return result


def clean_title(data):
    name = data[reader.ARTIST_COLUMN]
    title = data[reader.TITLE_COLUMN].strip().replace(nonBreakSpace, " ")
    rule = get_rule_for_title(name, title)
    while rule:
        title = rule['new_title']
        rule['count'] += 1
        rule = get_rule_for_title(name, title)
    return title


def clean_year(data):
    name = data[reader.ARTIST_COLUMN]
    title = data[reader.TITLE_COLUMN]
    year = data[reader.SONG_YEAR_COLUMN]
    if year <= 1800:
        # check if the song exists
        artist_id = db.artist_repository.get_id(name, should_insert=False)
        if artist_id:
            song_id = db.song_repository.get_id(artist_id, title, year, should_insert=False)
            if song_id:
                song = db.song_repository.read_rowid(song_id)
                year = song['year']
        rule = get_rule_for_year(name, title, year)
        while rule:
            year = rule['new_year']
            rule['count'] += 1
            rule = get_rule_for_year(name, title, year)
    return year


def get_rule_for_artist_only(artist):
    for rule in db.swaprule_repository.rules_for_artist_only(artist):
        if rule['new_artist']:
            return rule
    return None


def get_rule_for_title(artist, title):
    for rule in db.swaprule_repository.rules_for_artist_only(artist):
        if rule['title'] == title and rule['new_title']:
            return rule
    return None


def get_rule_for_year(artist, title, year):
    for rule in db.swaprule_repository.rules_for_artist_only(artist):
        if rule['title'] == title and rule['year'] == year and rule['new_year']:
            return rule
    return None


