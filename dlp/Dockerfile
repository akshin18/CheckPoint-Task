FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing .pyc files
ENV PYTHONUNBUFFERED 1         # Ensures stdout and stderr are sent to Docker logs

WORKDIR /task

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

COPY ./requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . ./