FROM python:3.12-slim-bullseye

COPY . /src/

WORKDIR /src

RUN apt-get update && apt-get upgrade -y && apt-get install ffmpeg -y && apt-get install wget -y && apt-get install zip unzip -y

RUN wget "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"

RUN unzip -q maestro-v3.0.0-midi.zip && mkdir -p data && mv maestro-v3.0.0 data/midi

RUN rm maestro-v3.0.0-midi.zip

RUN pip3 install -r requirements.txt

RUN mkdir -p data/tokens

RUN mkdir -p data/midi_from_tokens

WORKDIR /src/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health