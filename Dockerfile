FROM python:3.8

WORKDIR /app
COPY requiirements.txt /app/requirements.txt

RUN apt-get update\
    && apt-get install gcc -y \
    && app-get clean

RUN pip install virtualenv
RUN virtualenv env

RUN env/bin/pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./sql_ordersheet/* /app/sql_ordersheet/

ENTRYPOINT /app/env/bin/uvicorn sql_ordersheet.main:app --reload
