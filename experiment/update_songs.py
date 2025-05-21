import csv_experiment, sqlite3

conn = sqlite3.connect('datawarehouse.sqlite')


def combine(old, new):
	sqlupdate = 'UPDATE FACT SET FKSong=? WHERE FKSong=?'
	sqldelete = 'DELETE FROM Song WHERE ID=?'
	cursor = conn.cursor()
	cursor.execute(sqlupdate, (new, old))
	cursor.execute(sqldelete, (old, ))
	conn.commit()

filename = 'songs.csv'
with open(filename, 'r') as f:
	reader = csv_experiment.reader(f, delimiter=';')
	for row in reader:
		ratio = float(row[4])
		if row[0]:
			print row
			combine(row[2], row[0])