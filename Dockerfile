FROM python:3.11-alpine

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./bot /bot

WORKDIR /bot

RUN python3 __main__.py
