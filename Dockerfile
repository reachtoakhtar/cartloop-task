FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl

RUN apt-get update && \
	apt-get install -y --no-install-recommends gcc python3-dev musl-dev \
	libcurl4-openssl-dev libssl-dev default-libmysqlclient-dev build-essential \
	nano curl

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip --default-timeout=1000 install -r requirements.txt

ADD . /code/
RUN ls -alh

EXPOSE 8000
