import paho.mqtt.client as mqtt
import time

class LightBulbMQTTClient(mqtt.Client):
    def __init__(self, client_name):
        super(LightBulbMQTTClient, self).__init__(client_name)


    def on_log(self, client, userdata, level, buf):
        print(f"log {buf}")
        pass

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("Connected")
        else:
            print("Couldn't connect to broker!")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(f"Disconnected result code {str(rc)}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        if topic == f"command-{client.id}":
            if m_decode == "ON":
                self.stan = 1
            elif m_decode == "OFF":
                self.stan = 0
            print(f"Status set to: {self.stan}")
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")