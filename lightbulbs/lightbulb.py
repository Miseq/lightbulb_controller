from lightbulbs.lightbulb_mqtt_client import LightBulbMQTTClient
import main
import sys
import paho.mqtt.client as mqtt
from _thread import start_new_thread
import threading
import time

class LightBulb(mqtt.Client):
    def __init__(self,id, broker_address='localhost', stan=0):
        super(LightBulb, self).__init__(id)
        self._id = id
        self._stan = stan #0:OFF 1:ON
        self.broker_address = broker_address
    @property
    def id(self):
        return self._id

    @property
    def stan(self):
        return self._stan

    @stan.setter
    def stan(self, new_stan):
        if new_stan != 1 and new_stan != 0:
            raise ValueError("Wrong input, correct values are 0 for OFF and 1 for ON!")
        self._stan = new_stan

    def show_current_status(self):
        print(f"Status of lightbulb {self.id}", end="")
        while True:
            current_status = 'ON' if self.stan==1 else 'OFF'
            print(f"{current_status}")

    def change_status(self, new_status):
        self.stan = new_status
        self.publish(f"status-{self.id}", f'{self.stan}')

    def end_connection(self):
        self.publish("deactivation", self.id)
        self.disconnect()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        print("topic")
        if topic == f"command-{client.id}" or topic == "command-all":
            if m_decode == "ON" or m_decode == '1':
                self.change_status(1)
            elif m_decode == "OFF" or m_decode == '0':
                self.change_status(0)
            print(f"Status set to: {self.stan}")
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")

    def on_log(self, client, userdata, level, buf):
        #print(f"log {buf}")
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("Subscribing")
        self.subscribe(f"command-{self.id}")
        self.subscribe("command-all")
        self.publish("activation", self.id)
        self.publish(f"status-{self.id}", f'{self.stan}')


def main(*args, **kwargs):
    broker='localhost'
    client = LightBulb("Alfa")
    show_status = threading.Thread(target=client.show_current_status())
    show_status.run()
    print(f"connecting to brokrer {broker}")
    client.connect(broker)
    client.loop_start()
    while True:
        if input("DASD") == 0:
            break
        print(client.stan)
    client.loop_stop()


    client.end_connection()


if __name__ == '__main__':
    main()