FROM python:3.12-slim-bullseye

COPY . /src/

WORKDIR /src

RUN apt update && apt upgrade -y && apt install ffmpeg -y && apt install wget -y && apt install unzip -y && apt install fluidsynth -y

RUN wget "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip"

RUN unzip -q maestro-v3.0.0-midi.zip && mkdir -p data && mv maestro-v3.0.0 data/midi

RUN rm maestro-v3.0.0-midi.zip

RUN pip3 install -r requirements.txt

WORKDIR /src/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health