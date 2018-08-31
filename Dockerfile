#TODO: use alpine?
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD bot.py /code/