FROM frolvlad/alpine-python3
MAINTAINER Dickson Ukang'a
LABEL version="0.1"

RUN mkdir -p /srv/app
ADD requirements.pip /srv/app/requirements.pip
ADD controller.py   /srv/app/controller.py

RUN pip install -r /srv/app/requirements.pip

ENTRYPOINT ["python3", "/srv/app/controller.py"]
