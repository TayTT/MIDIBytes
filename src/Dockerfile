FROM python:3.12-slim-bullseye

COPY . /src/

WORKDIR /src

RUN mkdir -p data/model

WORKDIR /src/data/model

RUN apt update --fix-missing && apt upgrade -y && apt install wget -y && apt install unzip -y

RUN wget -O model.zip "https://www.dropbox.com/scl/fi/hknnj6xk1jjb3v0it5t63/model.zip?rlkey=fulgjx73e3n1rnzr7d34f5kkt&st=9hgg7d5o"

RUN unzip -q model.zip && rm model.zip

RUN apt install ffmpeg -y && apt install fluidsynth -y

WORKDIR /src

RUN pip3 install -r requirements.txt

WORKDIR /src/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health