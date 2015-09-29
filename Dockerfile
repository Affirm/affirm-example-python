FROM ubuntu:12.04
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
RUN pip install -U flask-script gevent gunicorn

# copy code to /affirm
ADD . /affirm/affirm-example-python
WORKDIR /affirm/affirm-example-python

# TODO mount app.yml
RUN python setup.py install

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=16", "-k", "gevent" , "affirm_example.manage:app"]
