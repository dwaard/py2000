# to build: docker build --rm -t bugslayer/py2000-notebook .
# to run: docker run --rm -p 8888:8888 -v C:/code/python/py2000:/home/jovyan/work bugslayer/py2000-notebook
FROM jupyter/minimal-notebook:latest
USER root
RUN sudo apt-get update
RUN sudo apt-get -y install gcc

RUN pip install matplotlib
RUN pip install xlrd
RUN pip install xlwt
RUN pip install xlutils
RUN pip install openpyxl
RUN pip install python-Levenshtein
RUN pip install pandas
RUN pip install numpy
RUN pip install pillow
RUN pip install wordcloud
RUN pip install deep-translator


