FROM frolvlad/alpine-python3

MAINTAINER Dickson Ukang'a

LABEL version="0.1.0"

RUN mkdir -p /srv/app

ADD requirements.txt /srv/app/requirements.txt
ADD controller.py   /srv/app/controller.py

RUN pip install -r /srv/app/requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3", "/srv/app/controller.py"]
