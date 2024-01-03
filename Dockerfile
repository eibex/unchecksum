FROM python:3.12

COPY ./ /unchecksum/

RUN python3.12 -m pip install -r /unchecksum/requirements.txt

WORKDIR /unchecksum

ARG dir1

ARG dir2

CMD ["python3.12", "-u", "unchecksum.py ${dir1} -cc ${dir2}"]
