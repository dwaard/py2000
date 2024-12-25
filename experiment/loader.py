import sqlite3;
from datetime import datetime

from staging import StagedData


def build_db():
    conn = sqlite3.connect('output/top2000.sqlite')
    c = conn.cursor()
    c.execute("drop table if exists ARTIST")
    c.execute("drop table if exists SONG")
    c.execute("drop table if exists OCCURRENCE")
    c.execute("create table ARTIST (name TEXT)")
    c.execute("create table SONG (artist_id INT, title TEXT , year INT)")
    c.execute("create table OCCURRENCE (song_id INT, edition INT, position INT)")
    return conn


def insert_artist(conn, artist_name):
    c = conn.cursor()
    c.execute("insert into ARTIST values (?)", (artist_name,))
    return c.lastrowid


def insert_song(conn, artist_id, title, year):
    c = conn.cursor()
    c.execute("insert into SONG values (?, ?, ?)", (artist_id, title, year))
    return c.lastrowid


def insert_occurrence(conn, song_id, edition, position):
    c = conn.cursor()
    c.execute("insert into OCCURRENCE values (?, ?, ?)", (song_id, edition, position))


def load_into_db():
    a = datetime.now()
    print "Load staged data into SQLite database"
    s = StagedData()
    conn = build_db()
    for artist_name, artist_dict in s.cache_analyze_data().iteritems():
        artist_id = insert_artist(conn, artist_name)
        for song_title, song_info in artist_dict.iteritems():
            year = song_info.get('year')
            song_id = insert_song(conn, artist_id, song_title, year)
            for edition in range(1999, 2017):
                position = 0
                if edition in song_info:
                    position = song_info[edition]
                insert_occurrence(conn, song_id, edition, position)
            song_id += 1

        artist_id += 1
    conn.commit()
    conn.close()
    b = datetime.now() - a
    delta = 1.0 * b.total_seconds() + b.microseconds * 0.0000001
    print "Finished loading in %.3f seconds" % delta

load_into_db()