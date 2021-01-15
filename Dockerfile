FROM python:latest

RUN mkdir /home/lightbulb
WORKDIR /home/lightbulb
ADD ./lightbulbs/ /home/lightbulb
ADD ./requirements.txt /home/lightbulb
ENV ID=Alfa
ENV BROKER=broker.hivemq.com
ENV STATUS=ON
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python lightbulb_interface.py -status=$STATUS -broker=$BROKER -id=$ID"]
