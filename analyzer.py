import difflib
import Levenshtein
import unicodedata
from staging import *

stems = dict()

def analyze_all():
    s = StagedData()
    a = ArtistFile()
    c = SongFile()
    cache = s.cache_analyze_data()
    artists = cache.keys()
    for artist in artists:
        stems[artist] = stem(artist)
    length = len(artists)
    size = fac(length-1) # determine number of checks
    print "Analyzing %i artists. This means %d similiarity checks" % (length, size)
    similar_artist_file = codecs.open("staged/similar_artists.csv", encoding='cp1252', mode='w')
    line = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (
        'name1', 'name2', 'artist', 'songs', 'adv', 'stem1', 'stem2')
    similar_artist_file.write(line)
    similar_song_file = codecs.open("staged/similar_songs.csv", encoding='cp1252', mode='w')
    count = 1
    done = 0
    for name, songs in cache.iteritems():
        perc = 100.0 * done / size
        print " " * 79 + '\r',
        print "Analyzing: " + '{:.1f}% '.format(perc) + repr(name) + " %d" % len(songs),
        analyze_artist(name, cache.keys()[count:], a, similar_artist_file, cache)
        analyze_artist_songs(name, songs, c, similar_song_file)
        count += 1
        done += (length - count)
    print " " * 79 + '\r',
    print "Analyzing: 100.00%"
    similar_song_file.close();


def analyze_artist(name1, other_artists, a, file, cache):
    for name2 in other_artists:
        if not a.should_ignore_on_analyze(name1, name2):
            stem1 = stems[name1]
            stem2 = stems[name2]
            r = similar(stem1, stem2)
            if r >= 0.52:
                song_r = closest_songs_ratio(cache[name1].keys(), cache[name2].keys())
                if r > 0.91 or song_r > 0.8:
                    adv = "misschien"
                    if r>0.91 or r>0.8 and song_r>0.8:
                        adv = "zeker"
                    number = "%f" % r
                    number = number.replace(".", ",")
                    number2 = "%f" % song_r
                    number2 = number2.replace(".", ",")
                    line = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (
                        name1, name2, number, number2, adv, stem1, stem2)
                    file.write(line)


def closest_songs_ratio(songs1, songs2):
    result = 0.0
    for song in songs1:
        closest = difflib.get_close_matches(song, songs2)
        if len(closest) == 0:
            closest = u''
        else:
            closest = closest[0]
        ratio = Levenshtein.ratio(song, closest)
        if ratio>result:
            result = ratio
    return result


def analyze_artist_songs(name, songs, c, file):
    if len(songs) > 1:
        index = 0
        for song1 in songs.keys():
            name1 = "%s - %s" % (song1, name)
            for song2 in songs.keys()[index + 1:]:
                stem1 = stem(song1)
                stem2 = stem(song2)
                if not c.should_ignore_on_analyze(name1, song2):
                    r = similar(stem1, stem2)
                    if (r >= 0.75):
                        number = "%f" % r
                        number = number.replace(".", ",")
                        line = '"%s";"%s";"%s";"%s";"%s";"%s"\n' % (
                            name, song1, song2, songs[song1]['year'], songs[song2]['year'], number)
                        file.write(line)
            index += 1


def similar(a, b):
    return Levenshtein.ratio(a, b)


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

def fac(n):
	r = 0;
	for n in range(0,n):
		r = r + n
	return r


def capital_count(s):
    return sum(1 for c in s if c.isupper())



