FROM python:3.11

LABEL maintainer="Aashish Dahran"


ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip \
        build-essential \
        postgresql-client \
        libpq-dev \
        gcc \
        python3-dev \
    && pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi \
    && apt-get remove -y gcc libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/*


COPY ./app /app

EXPOSE 8000
