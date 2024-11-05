FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/api

RUN pip install --upgrade pip && pip install poetry

COPY ./pyproject.toml ./
COPY ./poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --timeout 120

COPY . ./

EXPOSE 8000

CMD uvicorn api.app:app --host 0.0.0.0 --port 8000 --proxy-headers

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]