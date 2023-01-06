FROM ubuntu:20.04
LABEL maintainer "Asher Pembroke <apembroke@predsci.com>"

RUN apt update
RUN apt install -y python3-pip git


# extra stuff for debugging (remove after in full production)
RUN apt install -y htop traceroute iproute2 iputils-ping


ADD . /dashboard

WORKDIR /dashboard

RUN pip install -r requirements.txt

RUN pip install -e .
