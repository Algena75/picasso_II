FROM python:3.10-slim

# RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./README.md /app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
#RUN pip install --upgrade pip
#RUN pip install gunicorn
RUN apt update && pip install poetry==1.7.0 \
    && poetry config virtualenvs.create false \
    && poetry install --without test --no-interaction --no-ansi \
    && mkdir backend docker

ADD ./backend /backend/
ADD ./docker /docker/

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
