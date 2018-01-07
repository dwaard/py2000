import matplotlib.pyplot as plt

import db

sql = 'SELECT A.name, count(S.rowid) AS songcount, SUM(2000 - O.position) AS score, MIN(O.position) AS highest ' \
      'FROM OCCURANCE O INNER JOIN Song S ON O.song = S.rowid INNER JOIN Artist A ON S.artist = A.rowid ' \
      'WHERE edition=2017 GROUP BY A.name ORDER BY score DESC LIMIT 100'

x = []
y = []
sizes = []
names = []
for row in db.raw_sql(sql):
    names.append(row[0])
    sizes.append(row[1] * 10)
    y.append(row[2])
    x.append(row[3])

plt.scatter(x, y, s=sizes)
plt.show()
