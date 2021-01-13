FROM python:latest

RUN mkdir /home/controller
WORKDIR /home/controller
ADD ./ /home/controller

RUN pip install -r requirements.txt
