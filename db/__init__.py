import sqlite3
import os
import pandas as pd

from db.artist_repository import ArtistRepository
from db.song_repository import SongRepository
from db.occurrence_repository import OccurrenceRepository
from db.swaprule_repository import SwapruleRepository
from db.ignorerule_repository import IgnoreruleRepository

# the connection to the database
_conn = sqlite3.connect(os.path.join('staged', 'db.sqlite'))

# create the repositories
artist_repository = ArtistRepository(_conn)
song_repository = SongRepository(_conn)
occurrence_repository = OccurrenceRepository(_conn)
swaprule_repository = SwapruleRepository(_conn)
ignorerule_repository = IgnoreruleRepository(_conn)


def append(artist_name, song_title, song_year, edition_year, edition_position):
    artist_id = artist_repository.get_id(artist_name)
    # print "%s: %s" % (artist_id, artist_name)
    song_id = song_repository.get_id(artist_id, song_title, song_year)
    # print "%s: %s" % (song_id, song_title)
    occurrence_repository.append([song_id, edition_year, edition_position])


def get_song_by_name_and_title(artist_name, song_title):
    artist_id = artist_repository.get_id(artist_name)
    # print "%s: %s" % (artist_id, artist_name)
    song_id = song_repository.get_id(artist_id, song_title, song_year)
    # print "%s: %s" % (song_id, song_title)


def dataframe(sql='', params={}):
    return pd.read_sql_query(sql, _conn, params=params)

def all_rows(where='1'):
    sql = "SELECT A.name, S.title, S.year, O.edition, O.position FROM OCCURANCE O " \
          "INNER JOIN Song S ON O.song = S.rowid INNER JOIN Artist A ON S.artist = A.rowid " \
          "WHERE %s ORDER BY A.name, S.title, O.edition" % where
    c = _conn.cursor()
    for row in c.execute(sql):
        yield row

def raw_sql(sql=''):
    c = _conn.cursor()
    for row in c.execute(sql):
        yield row


def commit():
    _conn.commit()