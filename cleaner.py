from datetime import datetime
from difflib import SequenceMatcher
from staging import *

artist_dictionary_filename = "staged/artist_dictionary.xls"

def analyze_songs():
    a = datetime.now()
    print "Start analyzing staged environment"
    s = StagedData()
    c = SongFile()
    cache = s.cache_analyze_data()
    artists = cache.keys()
    a_ignore = ArtistIgnoreList()
    s_ignore = SongIgnoreList()
    length = len(artists)
    print "Analyzing %i artists." % length
    size = length # determine number of checks
    similar_artist_file = codecs.open("staged/similar_artists.csv", encoding='utf8', mode='w')
    similar_song_file = codecs.open("staged/similar_songs.csv", encoding='utf8', mode='w')
    count = 1
    for name, songs in cache.iteritems():
        perc = 100.0 * count / size
        count += 1
        #analyze_artist(name, cache.keys()[count:], a_ignore, similar_artist_file)
        analyze_artist_songs(name, songs, c, similar_song_file)
        print " " * 79 + '\r',
        print "Analyzing: " + '{:.1f}% '.format(perc) + repr(name) + " %d" % len(songs),
    print " " * 79 + '\r',
    print "Analyzing: 100.00%"
    similar_song_file.close();
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished analyzing in %.3f seconds" % delta


def analyze_artist(name1, other_artists, ignorelist, file):
    for name2 in other_artists:
        if not ignorelist.contains(name1, name2):
            r = similar(name1, name2)
            if (r >= 0.8):
                line = '"%s";"%s";"%f"\n' % (
                    name1, name2, r)
                file.write(line)


def analyze_artist_songs(name, songs, c, file):
    if len(songs) > 1:
        index = 0
        for song1 in songs.keys():
            name1 = "%s - %s" % (song1, name)
            for song2 in songs.keys()[index + 1:]:
                if not c.should_ignore_on_analyze(name1, song2):
                    r = similar(song1, song2)
                    if (r >= 0.8):
                        line = '"%s";"%s";"%s";"%f"\n' % (
                            name, song1, song2, r)
                        file.write(line)
            index += 1


def analyze_artists():
    a = datetime.now()
    # Do stuff here
    print "Start analyzing staged environment"
    s = StagedData()
    artists = s.get_artists()
    ignorelist = ArtistIgnoreList()
    length = len(s)
    print "Analyzing %i artists." % length
    size = fac(length) # determine number of checks
    filename = "staged/similar_songs.csv"
    myfile = codecs.open(filename, encoding='utf8', mode='w')
    count = 1
    for index, song1 in enumerate(s):
        perc = 100.0 * count / size
        name1 = "%s - %s" % (song1[0], song1[1])
        print " " * 79 + '\r',
        print "Analyzing: " + '{:.1f}% '.format(perc) + repr(name1),

        for song2 in s[count+1:]:
            count += + 1
            name2 = "%s - %s" % (song2[0], song2[1])
            if not ignorelist.contains(name1, name2):
                r = similar(name1, name2)
                if (r >= 0.8):
                    line = '"%s";"%s";"%f"\n' % (
                    name1, name2, r)
                    myfile.write(line)
    print " " * 79 + '\r',
    print "Analyzing: 100.00%"
    myfile.close();
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished analyzing in %.3f seconds" % delta


def make_artist_dictionary():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('test')

    with open("staged/similar.csv", "rb") as csvFile:
        xlrow = 0
        for row in UnicodeReader(csvFile, encoding="utf8", delimiter=';', quoting=csv.QUOTE_NONNUMERIC):
            if(float(row[2])>=1.0):
                if should_swap_artists(row):
                    swap_artists(row)
                sheet.write(xlrow, 0, label=row[0])
                sheet.write(xlrow, 1, label=row[1])
                sheet.write(xlrow, 2, label=row[2])
                xlrow = xlrow + 1
    workbook.save(artist_dictionary_filename)


def should_swap_artists(row):
    return capital_count(row[0])  > capital_count(row[1])


def capital_count(s):
    return sum(1 for c in s if c.isupper())

def swap_artists(row):
    s = row[0]
    row[0] = row[1]
    row[1] = s


def clean():
    a = datetime.now()
    # Do stuff here
    print "Start cleaning staged environment"

    # Print processing time
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished cleaning in %.3f seconds" % delta


def get_artists():
    print "Reading all artists"
    s = set()
    for row in data():
        s.add(row[1])
    return list(s)

def data():
    with open("staged/data.csv", "rb") as csvFile:
        for row in UnicodeReader(csvFile, encoding="utf8", delimiter=';', quoting=csv.QUOTE_NONNUMERIC):
            yield(row)  # yield the data


def fac(n):
	r = 0;
	for n in range(0,n):
		r = r + n
	return r

def similar(a, b):
    return SequenceMatcher(None, stem(a), stem(b)).ratio()

def stem(s):
    s = s.strip()
    s = s.lower()
    if s.startswith("the "):
        s = s[4:]
    if s.startswith("de "):
        s = s[3:]

    return (s.replace(" the ", "")
                .replace(" de ", "")
                .replace(" and ", "")
                .replace(" en ", "")
                .replace(" & ", "")
                )

#make_artist_dictionary()
analyze_songs()
#clean()