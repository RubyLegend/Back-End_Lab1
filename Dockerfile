FROM python:3.10.8

ENV FLASK_APP="stealth_webpage"

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY stealth_webpage /opt/stealth_webpage

WORKDIR /opt

CMD flask run --host 0.0.0.0 -p $PORT