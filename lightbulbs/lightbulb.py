from lightbulbs.lightbulb_mqtt_client import LightBulbMQTTClient
import main
import paho.mqtt.client as mqtt
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

    def connect_to_broker(self):
        if self.is_connected():
            return  # jeśli jest już połączony to opuszczamy metodę
        self.connect(self.broker_address)
        self.loop_start()
        self.subscribe(f"command-{self.id}")
        self.publish("activation", self.id)
        self.publish(f"status-{self.id}", f'{self.stan}')
        self.publish(f"command-{self.id}", f'{self.stan}')
        self.loop_stop()

    def change_status(self, new_status):
        if not self.is_connected():
            self.reconnect()
            self.stan = new_status
            self.loop_start()
            self.publish(f"status-{self.id}", f'{self.stan}')
            self.loop_stop()

    def end_connection(self):
        self.loop_start()
        self.publish("deactivation", self.id)
        self.loop_stop()
        self.disconnect()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        if topic == f"command-{client.id}":
            if m_decode == "ON" or m_decode == 1:
                self.stan = 1
            elif m_decode == "OFF" or m_decode == 0:
                self.stan = 0
            print(f"Status set to: {self.stan}")
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")

    def on_log(self, client, userdata, level, buf):
        #print(f"log {buf}")
        pass

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("Connected")
        else:
            print("Couldn't connect to broker!")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(f"Disconnected result code {str(rc)}")

def main(*args, **kwargs):
    broker='localhost'
    client = LightBulb("Alfa")
    print(f"connecting to brokrer {broker}")
    client.connect_to_broker()

    client.disconnect()


if __name__ == '__main__':
    main()