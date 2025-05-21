import os, sys, sqlite3, codecs

conn = sqlite3.connect('datawarehouse.sqlite')

cursor = conn.cursor()
cursor.execute('SELECT * FROM RAW WHERE Artist LIKE "%& Bl%" LIMIT 10')
artists = cursor.fetchall()

filename = "test.txt"
try:
    os.remove(filename)
except OSError:
    pass
myfile = codecs.open(filename, encoding='utf-8', mode='w')
myfile.write(u'\u4500 blah blah bla\n')

for index1 in range(len(artists)):
    x = artists[index1][1]
    print (repr(x))
    myfile.write(x + "\n")

myfile.close()