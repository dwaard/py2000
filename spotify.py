import spotipy, json
from staging import StagedData
import os.path
import time


s = StagedData()
spotify = spotipy.Spotify()

def create_cache_filename(artist_name):
    return 'staged/spotify_cache/artist_%s.json' % artist_name.lower().replace("/", "_").replace("?", "")

def create_track_filename(artist_name, track_name):
    filename = artist_name + "-" + track_name
    return 'staged/spotify_cache/track_%s.json' % filename.lower().replace("/", "_").replace("?", "")


def file_exists(artist_name):
    return os.path.exists(create_cache_filename(artist_name))

for artist_name, artist_dict in s.cache_analyze_data().iteritems():
    print "Fetching: %s" % artist_name
    filename = create_cache_filename(artist_name)
    if not file_exists(filename):
        results = spotify.search(q='artist:' + artist_name, type='artist')
        obj = open(filename, 'w')
        obj.write(json.dumps(results, sort_keys=True,
                     indent=4, separators=(',', ': ')))
        obj.close
        time.sleep(0.25)
    for song_title, song_info in artist_dict.iteritems():
        filename = create_track_filename(artist_name, song_title)
        if not file_exists(filename):
            results = spotify.search('track:%s' % song_title, type='track')
            obj = open(filename, 'w')
            obj.write(json.dumps(results, sort_keys=True,
                                 indent=4, separators=(',', ': ')))
            obj.close
            time.sleep(0.25)

results = spotify.search(q='track:under pressure AND artist:Queen AND market:NL', type='track')
obj = open(create_cache_filename("___AAA1"), 'w')
obj.write(json.dumps(results, sort_keys=True,
             indent=4, separators=(',', ': ')))
obj.close

# for artist_name, artist_dict in s.cache_analyze_data().iteritems():
#     print artist_name + " :",
#     data = ""
#     with open(create_cache_filename(artist_name)) as data_file:
#         try:
#             #     print artist["name"]
#             # for artist in data["artists"]["items"]:
#             data = json.load(data_file)
#             length = len(data["artists"]["items"])
#         except ValueError:
#             length = 0
#     print length