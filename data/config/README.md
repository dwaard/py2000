# Coniguration folder
This folder contains config data of the editions. Each edition config must be placed in a file called `[edition_year].yml` (i.e. 2016.yml) an must be structured like:
```yml
filename: YOUR-FILENAME-HERE
# File configuration settings. Default values are provided; adjust as needed.
fileconfig:
  start_row: 2
  position_col: 1
  artist_col: 2
  title_col: 3
  year_col: 4
# Minimum ratio of certain matches required. Lower this to the lowest acceptable value,
# which should at least include the lowest match listed in the problems list.
min_certain_ratio: 0.9
# Minimum ratio of relevant matches required. Increase this to the highest acceptable value.
# This should be higher than the index of the highest incorrect match after all the manual matches 
# are listed.
min_relevant_ratio: 0.63
# Manual matches to pick the ones that are between incorrect matches in the problems list. The
# poblem list is formatted such that lines can be copied directly here.
manual_matches: []
```