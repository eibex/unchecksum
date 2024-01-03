FROM python:3.12

COPY ./ /unchecksum/

RUN python3.12 -m pip install -r /unchecksum/requirements.txt

WORKDIR /unchecksum
