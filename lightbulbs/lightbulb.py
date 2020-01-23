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
        current_status = 'ON' if self.stan==1 else 'OFF'
        return f"Status:{current_status}"

    def change_status(self, new_status):
        self.stan = new_status
        self.publish(f"status-{self.id}", f'{self.stan}')

    def on_disconnect(self):
        self.publish("deactivation", self.id)
        self.disconnect()
        print("Succesfully disconnected")

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
    print(f"connecting to brokrer {broker}")
    client.connect(broker)
    client.loop_start()
    time.sleep(0.5)
    print(f"Lightb {client.id}\nConnected: {client.is_connected()}\n{client.show_current_status()}")
    print("To show current status: type 'status', turning on/off type 'on' or 'off', to exit type 'e'")
    while True:
        x = input("- ").lower()
        if x == 'status' or x=='s':
            print(client.show_current_status())
        if x == 'on':
            client.change_status(1)
        if x == 'off':
            client.change_status(0)
        if x == 'exit' or x =='e':
            client.disconnect()
            break
    client.loop_stop()



if __name__ == '__main__':
    main()