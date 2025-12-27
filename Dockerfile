# to build: docker build --rm -t bugslayer/py2000-notebook .
# to run: docker run --rm -p 8888:8888 -v C:/code/python/py2000:/home/jovyan/work bugslayer/py2000-notebook
FROM jupyter/minimal-notebook:latest
USER root

RUN sudo apt-get update
RUN sudo apt-get -y install gcc

USER jovyan

RUN cd /home/jovyan/work
# RUN python -m venv .venv
# RUN source .venv/bin/activate
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /home/jovyan/work/


