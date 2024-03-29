FROM ubuntu:16.04
MAINTAINER Blaine Chatman <blaine.chatman@affirm.com>

# install deb/pip packages
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential \
                       software-properties-common \
                       python \
                       python-dev \
                       python-pip \
                       python-virtualenv && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
    apt-get clean

# copy code to /affirm
ADD . /affirm/affirm-example-python
WORKDIR /affirm/affirm-example-python

RUN pip install -U pip==19.2.3 # needs to be pinned to this version for python 2
RUN pip install -r requirements.txt # default version was not properly working

# TODO mount app.yml
RUN python setup.py install

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=16", "-k", "gevent" , "affirm_example.manage:app"]
