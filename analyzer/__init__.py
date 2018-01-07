import db

import unicodedata

import Levenshtein

import year_analyzer

year_analyzer = year_analyzer.YearAnalyzer()

def analyze_artists():
    print "Start analyzing artist names"
    data = []
    for row in db.artist_repository.read_all(order_by='name ASC'):
        row['stem'] = stem(row['name'])
        data.append(row)
    for index, artist in enumerate(data):
        analyze_artist(artist, data[index:])


def analyze_artists_songs():
    print "Start analyzing song titles of all artists"
    for row in db.artist_repository.read_all(order_by='name ASC'):
        analyze_artist_songs(row)


def analyze_artist_songs(artist, cutoff_ratio=0.7):
    data = []
    for row in db.song_repository.read_all(where='artist=?', params=[artist['rowid']]):
        row['stem'] = stem(row['title'])
        data.append(row)

    for index, song1 in enumerate(data):
        similar_songs = [song1]
        for song2 in data[index + 1:]:
            if song1["rowid"] != song2["rowid"] and \
                    db.ignorerule_repository.rulecount_for_songs(artist['name'], song1['title'], song2['title']) == 0:
                r = Levenshtein.ratio(song1['stem'], song2['stem'])
                if r >= cutoff_ratio:
                    similar_songs.append(song2)
        if len(similar_songs) > 1:
            handle_song_equality(artist, similar_songs)


def handle_song_equality(artist, data):
    print "-" * 80
    print "De volgende songtitels van %s lijken sterk op elkaar:" % artist['name']
    choice = -1
    while choice != 0 and len(data) > 1:
        for index, row in enumerate(data):
            print "%s: [%s](%d)" % (index+1, row['title'], row['year'])
        print "Welke hoort NIET in dit rijtje thuis?"
        choice = get_choice("(enter als alle titels hetzelfde liedje voorstellen): ")
        if choice > 0:
            data.remove(data[choice - 1])
        print ""
    # nu hebben we een setje met gelijke srtiestnamen
    if len(data) > 1:
        print "Welke van deze titels is de beste?"
        for index, row in enumerate(data):
            print "%s: %s" % (index+1, row['title'])
        choice = get_choice("(enter als deze vegelijking moet worden genegeerd): ")
        if choice > 0:
            choice -= 1
            new_title = data[choice]['title']
            for index, row in enumerate(data):
                if index != choice:
                    db.swaprule_repository.append([
                        artist['name'],
                        row['title'],
                        None,
                        None,
                        new_title,
                        None,
                        -1
                    ])
        else:
            for index, song1 in enumerate(data):
                for song2 in data[index + 1:]:
                    if song1['rowid'] != song2['rowid']:
                        db.ignorerule_repository.append([artist['name'], song1['title'], None, song2['title']])


def analyze_artist(artist1, other_artists):
    similar_artists = [artist1]
    for artist2 in other_artists:
        if artist1["rowid"] != artist2["rowid"] and \
                        db.ignorerule_repository.rulecount_for_artists(artist1['name'], artist2['name']) == 0:
            r = Levenshtein.ratio(artist1['stem'], artist2['stem'])
            if r >= 0.8:
                similar_artists.append(artist2)
    if len(similar_artists) > 1:
        handle_artist_equality(similar_artists)


def handle_artist_equality(data):
    print "-" * 80
    print "De volgende artiestnamen lijke sterk op elkaar:"
    choice = -1
    while choice != 0 and len(data) > 1:
        for index, row in enumerate(data):
            print "%s: %s" % (index+1, row['name'])
        print "Welke hoort NIET in dit rijtje thuis?"
        choice = get_choice("(enter als alle namen dezelfde artiest voorstellen): ")
        if choice > 0:
            data.remove(data[choice - 1])
        print ""
    # nu hebben we een setje met gelijke srtiestnamen
    if len(data) > 1:
        print "Welke van deze namen is de beste naam?"
        for index, row in enumerate(data):
            print "%s: %s" % (index+1, row['name'])
        choice = get_choice("(enter als deze vegelijking moet worden genegeerd): ")
        if choice > 0:
            choice -= 1
            new_name = data[choice]['name']
            for index, row in enumerate(data):
                if index != choice:
                    db.swaprule_repository.append([
                        row['name'],
                        None,
                        None,
                        new_name,
                        None,
                        None,
                        -1
                    ])
        else:
            for index, artist1 in enumerate(data):
                for artist2 in data[index + 1:]:
                    if artist1['rowid'] != artist2['rowid']:
                        db.ignorerule_repository.append([artist1['name'], None, artist2['name'], None])


def get_choice(text):
    strval = raw_input(text)
    try:
        return int(strval)
    except ValueError:
        return 0


def stem(s):
    # first, replace nasty unicode chars with ascii representations
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    # s = s.encode('ascii', errors='replace')
    s = s.strip() # remove all leading and trailing spaces
    s = s.lower() # change to lower case
    if s.startswith("the "): # remove leading the
        s = s[4:]
    if s.startswith("de "): # remove leading de
        s = s[3:]
    if s.startswith("les "): # remove leading de
        s = s[4:]
    # remove some other standard words
    s = (s.replace(" the ", " ")
            .replace(" de ", " ")
            .replace(" and ", " ")
            .replace(" en ", " ")
            .replace(" & ", " ")
            .replace("'", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace("-", " ")
            .replace("!", " ")
            .replace("?", " ")
            .replace(" feat", " ")
            .replace(" ft", " ")
    )
    while "  " in s:
        s = s.replace("  ", " ")
    return s
