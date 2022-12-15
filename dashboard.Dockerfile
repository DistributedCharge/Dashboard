FROM continuumio/miniconda3:latest
LABEL maintainer "Asher Pembroke <apembroke@predsci.com>"

RUN conda config --add channels conda-forge

RUN conda install python=3.7

RUN conda install jupyter jupytext

RUN pip install --user git+https://github.com/predsci/psidash.git
RUN pip install dash-bootstrap-components

ADD . /dashboard

WORKDIR /dashboard

RUN pip install -r requirements.txt

RUN pip install -e .
