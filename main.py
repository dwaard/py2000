from datetime import datetime
import sources2, codecs
from staging import StagedData
import analyzer


def extract():
    a = datetime.now()
    # Do stuff here
    print "Start extracting raw data into staged environment"
    staging = StagedData()
    for row in sources2.read_all():  # extract data into rows
        # clean and stage the data
        staging.append(row)
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished extracting in %.3f seconds" % delta


def analyze():
    a = datetime.now()
    print "Start analyzing staged environment"
    analyzer.analyze_all()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished analyzing in %.3f seconds" % delta


def load():
    a = datetime.now()
    print "Load staged data into database"
    s = StagedData()
    filename = "staged/output.csv"
    writer = codecs.open(filename, encoding='cp1252', mode='w')
    line = '"Artist";"Title";"Year";"Decade"'
    for y in range(1999,2017):
        line += ';"%s"' % y
    line += ';"Score"'
    writer.write(line + '\n')
    for artist_name, artist_dict in s.cache_analyze_data().iteritems():
        for song_title, song_info in artist_dict.iteritems():
            year = song_info.get('year')
            decade = "" + str((year % 100) / 10) + "0's"
            line = '"%s";"%s";"%s";"%s"' % (artist_name, song_title, year, decade)
            score = 0
            for y in range(1999, 2017):
                if y in song_info:
                    score += 2001 - song_info[y]
                    line += ';"%s"' % song_info[y]
                else:
                    line += ';"0"'
            line += ';"%d"' % score
            writer.write(line + '\n')
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished loading in %.3f seconds" % delta


extract()
analyze()
# load()