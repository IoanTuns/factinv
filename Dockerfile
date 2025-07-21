FROM python:3.11-slim-bookworm
LABEL maintainer="factinv"

ENV PYTHONUNBUFFERED=1

COPY ./req3.txt /requirements.txt
COPY . /factinv_app/
COPY ./scripts /scripts

WORKDIR /factinv_app

EXPOSE 80

RUN python -m venv /py_env && \
    /py_env/bin/pip install --upgrade pip && \
    /py_env/bin/pip install --upgrade setuptools 

RUN apt-get update
RUN apt-get install -y postgresql-client musl-dev libmagic1 libjpeg-dev zlib1g-dev

RUN /py_env/bin/pip install  --no-cache-dir -U -r /requirements.txt

RUN apt-get clean

RUN adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -RR 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/py_env/bin:$PATH"

USER app:app

CMD ["run.sh"]