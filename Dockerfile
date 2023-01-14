FROM python:3.10.8

ENV FLASK_APP="stealthwebpage"

ENV FLASK_DEBUG=$FLASK_DEBUG

ENV JWT_SECRET_KEY=156334938555886735294293839154925725084

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY stealthwebpage /opt/stealthwebpage

WORKDIR /opt

CMD flask run --host 0.0.0.0 -p $PORT
