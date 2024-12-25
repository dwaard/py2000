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
