import itertools
from reader.OpenPyXlReader import OpenPyXlReader

reader = OpenPyXlReader('raw/NPORadio2-Top-2000-2024.xlsx', 2024, start_row=2)

for row in itertools.islice(reader, 10):
    print(row)