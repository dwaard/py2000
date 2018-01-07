import numpy as np
import matplotlib.pyplot as plt

import db

MIN_YEAR = 1999
MAX_YEAR = 2017

start_year = 2008
end_year = 2011
step_size = 1
years = np.arange(start_year, end_year + 1, step_size)


num_bins = 20
data = []
labels = []
for y in years:
    data.append([y - row[2] for row in db.all_rows(where='edition=%s' % y)])
    labels.append('%s' % y)

plt.hist(data, num_bins, alpha=0.9, label=labels)

plt.title('Leeftijd van nummers in top2000')
plt.xlabel('leeftijd (jaren)')
plt.ylabel('Aantal nummers')
plt.legend(loc='upper right')
plt.show()

