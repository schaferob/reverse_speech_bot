#TODO: use alpine?
FROM ubuntu:18.04
RUN apt-get update
#put these high up in the docker file so they stay cached
#ffmpeg is pretty big; perhaps there is a smaller alternative to convert ogg->wav
RUN apt-get install -y ffmpeg
# use sox to reverse a wav
RUN apt-get install -y sox
RUN apt-get install -y python3
RUN apt-get install -y python3-pip


ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD bot.py /code/
