FROM ubuntu:20.04
LABEL maintainer "Asher Pembroke <apembroke@gmail.com>"

RUN apt update
RUN apt install -y python3-pip git


# extra stuff for debugging (remove after in full production)
RUN apt install -y htop traceroute iproute2 iputils-ping

# copy just the dependencies for faster dev builds
COPY requirements.txt /dashboard/requirements.txt

WORKDIR /dashboard

RUN pip install -r requirements.txt

# add everything else
ADD . /dashboard


# install in editable mode so code changes are live
RUN pip install -e .
