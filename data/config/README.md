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
# Minimum ratio of certain matches required. Lower this to the latest acceptable value,
# which should at least include the lowest match listed in the problems list.
min_certain_ratio: 0.99
# Minimum ratio of relevant matches required. Increase this to the latest acceptable value.
# This should be higher than the index of the highest incorrect match.
min_relevant_ratio: 0.50
# Manual matches to override automatic matching. The poblem list is formatted such that
# it can be copied directly here.
manual_matches: []
```