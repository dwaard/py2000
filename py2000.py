from datetime import datetime

import reader
import analyzer
import cleaner
import staging

import db


def truncate():
    a = datetime.now()
    print "Opschonen alle staging data"
    print "Occurrences..."
    db.occurrence_repository.truncate()
    print "Songs..."
    db.song_repository.truncate()
    print "Artists..."
    db.artist_repository.truncate()
    print "Swap rule counts..."
    db.swaprule_repository.reset_counts()
    db.commit()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Klaar met opschonen van de staging data in %.3f seconden" % delta
    print 80 * "-"


def extract():
    truncate()
    print "Extract alle ruwe data"
    a = datetime.now()
    # Do stuff here
    for row in reader.all_rows():  # extract data into rows
        row = cleaner.clean(row)
        db.append(
            row[reader.ARTIST_COLUMN],
            row[reader.TITLE_COLUMN],
            row[reader.SONG_YEAR_COLUMN],
            row[reader.EDITION_YEAR_COLUMN],
            row[reader.EDITION_POSITION_COLUMN]
        )
    db.swaprule_repository.save_rule_counts()
    db.commit()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Klaar met extracten van ruwe data in %.3f seconden" % delta
    print 80 * "-"


def analyze():
    a = datetime.now()
    print "Start analyseren van staging data"
    analyzer.analyze_artists()
    analyzer.analyze_artists_songs()
    analyzer.year_analyzer.start()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Klaar met analyseren in %.3f seconden" % delta
    print 80 * "-"
    analyzer.year_analyzer.handle_anomalies()


def export():
    a = datetime.now()
    # Do stuff here
    print "Start exporting staged data into csv"
    staged = staging.StagedData()
    for row in db.all_rows():  # extract data into rows
        # clean and stage the data
        staged.append(row)
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished exporting in %.3f seconds" % delta
    print 80 * "-"


if __name__ == "__main__":
    a = datetime.now()
    extract()
    analyze()
    export()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print 80 * "="
    print "Klaar in %.3f seconden" % delta
