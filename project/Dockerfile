FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing .pyc files
ENV PYTHONUNBUFFERED 1         # Ensures stdout and stderr are sent to Docker logs

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    netcat-openbsd \
    curl \
    && apt-get clean

RUN pip install --upgrade pip && pip install poetry

COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install

COPY . ./

EXPOSE 8000

#CMD gunicorn --bind 0.0.0.0:8000 project.wsgi:application