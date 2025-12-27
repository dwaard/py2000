# py2k
Import and analyze TOP2000 data. The projects consists of two parts:
- Command line tool for Extract-Transform-Load the data
- Jupyter notebook environment for data analysis

## Usage
### Setup
1. Create a `.env` file using the `.env.example`. 
1. Install Python and Venv

### Step 1: run the app
When you use venv:
1. Create the virtual environment using FIRST TIME ONLY
   `python -m venv .venv`
1. Activate venv using 
  - Windows: `.venv\Scripts\activate`
  - Linux: `source .venv/bin/activate`
1. When activated, you can install dependencies using `pip`:
  - For instance using the `requirements.txt` file: `pip install -r requirements.txt`
  - Or simply: `pip install <package-name>` (do NOT install globally)
1. Run the app: `python main.py`
  - You can do a dry-run by adding the `python main.py --pretend` switch
1. Deactivate when you're done: `deactivate` (Windows and Linux)



## Using Docker
When using Docker, the 
Building:
`docker build --rm -t bugslayer/py2000 .`
Running the main CLI tool:
`docker run -ti --rm -p 8888:8888 -v $(pwd):/home/jovyan/work bugslayer/py2000 python main.py`
Running Jupyter:
`docker run -ti --rm -p 8888:8888 -v $(pwd):/home/jovyan/work bugslayer/py2000`

# py2000
Python project to prepare top2000 data

# Dependencies

Dit script is afhankelijk van de volgende scripts:

- Levenshtein: `_path_to_\Continuum\anaconda2\python -m pip pip install python-Levenshtein`
- xlrd `_path_to_\Continuum\anaconda2\python -m pip pip install xlrd`
- xlwt `_path_to_\Continuum\anaconda2\python -m pip pip install xlwt`
- xlutils `_path_to_\Continuum\anaconda2\python -m pip pip install xlutlis`
- spotipy


# Docker support voor Jupyter
`docker build --rm -t bugslayer/t2k-notebook .`

`docker run --rm -p 8888:8888 -v C:/code/python/py2000:/home/jovyan/work bugslayer/t2k-notebook`

`docker run --rm -v C:/code/python/py2000:/home/jovyan/work python py2000.py`


## Editieprocessor
De editieprocessor klasse is bedoelt om de data van één T2k editie te importeren. 

Het proces is als volgt:

1. `new_entries`: maakt een nieuwe Song aan voor alle Occurances van liedjes die zijn uitgebracht in het jaar van de editie
1. `exact_match`: koppelt een Occurance aan een Song als één van de keys van de Song een exacte match (occ.key in song.keys) is
1. `manual_match`: een Occurance wordt gekoppeld aan een Song door een hardgecodeerde lijst
1. `direct_similarity`: koppel, op volgorde van _best passendheid_ de _best passende_ Song bij een occurance totdat de best passende kleiner is dan een ingestelde limiet. Deze limiet bepaalt dus vanaf waar we niet zeker zijn van een passende koppeling
1. `print_uncertain_matches`: (als er nog Occurances zijn die een similarity hebben groter dan de ingestelde minimaal relevante similarity) print makkelijk te kopieren info over deze kandidaat-koppelingen voor de manual_matchlist
1. `add_remaining_occurances_as_new_songs`: (als hierboven niet waar is) zoals de titel al zegt

## Werkwijze

1. Download databestand naar `RAW_FOLDER` 
1. Maak een config bestand aan in `CONFIG_FOLDER` door het voorbeeld te kopieren
1. Zet `min_certain_ratio` op 0.99 en `min_relevant_ratio` op 0.50
1. Run alle cellen tot en met de nieuwe. Er ontstaat een lijst met probleemgevallen
1. Check de probleemgevallen; begin bovenaan en verlaag `min_certain_ratio` zodat de laatst zekere ervan verdwijnt
1. Kijk vanaf onderen; Verhoog `min_relevant_ratio` totdat de laatste wel een match is
1. Er blijven nu maar een paar probleemgevallen over. Kopieer nu alle matches daaruit naar de parameter van `processor.process_manual_matches`
1. Als er geen match meer aanwezig is verhoog je `min_relevant_ratio` tot > de hoogst aanwezige ratio