FROM tensorflow/tensorflow

RUN mkdir /opt/api
WORKDIR /opt/api

RUN apt update

RUN pip install flask flask_restful requests pillow keras numpy

COPY ./api /opt/api