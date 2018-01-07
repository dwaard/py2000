import numpy as np
import matplotlib.pyplot as plt

import db

MIN_YEAR = 1999
MAX_YEAR = 2017

start_year = MAX_YEAR - 15
end_year = MAX_YEAR
step_size = 3
years = np.arange(start_year, end_year + 1, step_size)

num_bins = 20

for y in years:
    x = [row[2] for row in db.all_rows(where='edition=%s' % y)]
    plt.hist(x, num_bins, alpha=0.5, label='%s' % y)

plt.title('Uitgavejaar van nummers in top2000')
plt.xlabel('Uitgavejaar')
plt.ylabel('Aantal nummers')
plt.legend(loc='upper left')
plt.show()

