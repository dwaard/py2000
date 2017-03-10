import os, sys, codecs, sqlite3, math
from difflib import SequenceMatcher

conn = sqlite3.connect('datawarehouse.sqlite')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def myencode(a):
	return a.encode(sys.stdout.encoding, errors='replace')

def fac(n):
	r = 0;
	for n in range(0,n):
		r = r + n
	return r

def stem(s):
	return (s.strip().lower()
		.replace("the ", "")
		.replace(" & ", " "))

filename = "songs.csv"
try:
    os.remove(filename)
except OSError:
    pass
myfile = codecs.open(filename, encoding='utf8', mode='w')

for artist in conn.execute('SELECT * FROM ARTIST ORDER BY ID'):
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM SONG WHERE FKArtist=? ORDER BY ID', (artist[0], ))
	songs = cursor.fetchall()

	for index1 in range(len(songs)):
		name1 = stem(songs[index1][2])
		for index2 in range(index1+1,len(songs)):
			name2 = stem(songs[index2][2])
			r = similar(name1, name2)
			if (r >= 0.8):
				line = '"%i";"%s";"%i";"%s";"%f"\n' % (songs[index1][0], songs[index1][2], songs[index2][0], songs[index2][2], r)
				myfile.write(line)
print " " * 79 + '\r',
print "Analyzing: 100.00%"
myfile.close();
