FROM ubuntu:14.04
MAINTAINER Bo Ma

RUN echo "deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main" > /etc/apt/sources.list.d/deadsnakes.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DB82666C

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    mercurial \
    pkg-config \
    python3.4 \
    python3.4-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean

ADD https://raw.githubusercontent.com/pypa/pip/701a80f451a62aadf4eeb21f371b45424821582b/contrib/get-pip.py /root/get-pip.py
RUN sudo mkdir /app
ADD . /
RUN python3.4 /root/get-pip.py
RUN pip3.4 install -U "setuptools==15.1"
RUN pip3.4 install -U "pip==9.0.1"
RUN pip3.4 install -U "virtualenv==12.1.1"
RUN pip3.4 install -r requirements.txt
EXPOSE 5000
COPY . /app
WORKDIR /app
CMD []

ENTRYPOINT ["/usr/bin/python3.4"]