FROM python:3.12-slim-bullseye

COPY . /src/

WORKDIR /src

RUN apt-get update && apt-get upgrade && apt-get install wget -y && apt-get install zip unzip -y

RUN wget "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"

RUN unzip -q maestro-v3.0.0-midi.zip && mkdir -p data && mv maestro-v3.0.0 data/midi

RUN pip3 install -r requirements.txt

WORKDIR /src/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health