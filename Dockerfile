FROM python:latest

RUN mkdir /home/lightbulb
WORKDIR /home/lightbulb
ADD ./lightbulbs/ /home/lightbulb
ADD ./requirements.txt /home/lightbulb
ENV ID=Alfa
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python lightbulb_interface.py -id=$ID"]
