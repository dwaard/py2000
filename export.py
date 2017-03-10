import sqlite3, csv_experiment, os, codecs

conn = sqlite3.connect('datawarehouse.sqlite')
conn.text_factory = str ## my current (failed) attempt to resolve this
cur = conn.cursor()
data = cur.execute("""SELECT 
    Title, Name, Year,   
    sum(CASE WHEN edition = '1999' THEN position ELSE 0 END) as `1999`,
    sum(CASE WHEN edition = '2000' THEN position ELSE 0 END) as `2000`,
    sum(CASE WHEN edition = '2001' THEN position ELSE 0 END) as `2001`,
    sum(CASE WHEN edition = '2002' THEN position ELSE 0 END) as `2002`,
    sum(CASE WHEN edition = '2003' THEN position ELSE 0 END) as `2003`,
    sum(CASE WHEN edition = '2004' THEN position ELSE 0 END) as `2004`,
    sum(CASE WHEN edition = '2005' THEN position ELSE 0 END) as `2005`,
    sum(CASE WHEN edition = '2006' THEN position ELSE 0 END) as `2006`,
    sum(CASE WHEN edition = '2007' THEN position ELSE 0 END) as `2007`,
    sum(CASE WHEN edition = '2008' THEN position ELSE 0 END) as `2008`,
    sum(CASE WHEN edition = '2009' THEN position ELSE 0 END) as `2009`,
    sum(CASE WHEN edition = '2010' THEN position ELSE 0 END) as `2010`,
    sum(CASE WHEN edition = '2011' THEN position ELSE 0 END) as `2011`,
    sum(CASE WHEN edition = '2012' THEN position ELSE 0 END) as `2012`,
    sum(CASE WHEN edition = '2013' THEN position ELSE 0 END) as `2013`,
    sum(CASE WHEN edition = '2014' THEN position ELSE 0 END) as `2014`,
    sum(CASE WHEN edition = '2015' THEN position ELSE 0 END) as `2015`,
    sum(CASE WHEN edition = '2016' THEN position ELSE 0 END) as `2016`
FROM FACT INNER JOIN SONG ON FACT.FKSong=SONG.ID INNER JOIN ARTIST ON SONG.FKArtist=ARTIST.ID
GROUP BY FKSong""")

filename = "output.csv"
try:
    os.remove(filename)
except OSError:
    pass
myfile = codecs.open(filename, encoding='latin-1', mode='w')

myfile.write('"Titel";"Artiest";"Jaar";"1999";"2000";"2001";"2002";"2003";"2004";"2005";"2006";"2007";"2008";"2009";"2010";"2011";"2012";"2013";"2014";"2015";"2016"')
for row in data:
	print repr(row)
	myfile.write('"%s";"%s";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i";"%i"' % ([s.decode('latin-1') for s in row]))