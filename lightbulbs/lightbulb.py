import time
import paho.mqtt.client as mqtt


class LightBulb(mqtt.Client):

    def __init__(self, id, broker, status):
        super(LightBulb, self).__init__(id)
        self._id = id  # zakladam ze bedzie tekstem, w budynku lb raczej bd nazwane "front-1" || "portiernia"
        self._status = status
        self.broker = broker

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status != 'ON' and new_status != 'OFF':
            raise ValueError("Wrong input, correct values are 0 for OFF and 1 for ON!")
        self._status = new_status

    def show_current_status(self):
        return f"Status:{self.status}"

    def change_status(self, new_status):
        self.status = new_status
        self.publish(f"status-{self.id}", f'{self.status}', retain=True)
        print(f"Status changed to: {self.status}")

    def on_disconnect(self):
        self.publish("nonactive", self.id)  # TODO dodać usuwanie na disconnecta w tablicy sql
        print("Succesfully disconnected")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("\nMessage from broker recived: ", end="")
        print(topic)
        if topic == f"command-{client.id}" or topic == "command-all":
            if m_decode == "ON":
                self.change_status('ON')
            elif m_decode == "OFF":
                self.change_status('OFF')
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subscribing to: command-{self.id} and command-all")
        self.subscribe(f"command-{self.id}")
        self.subscribe("command-all")
        self.publish("active", self.id, retain=True)
        self.publish(f"status-{self.id}", f'{self.status}', retain=True)

    def connect_to_broker(self):
        print(f"connecting to brokrer {self.broker}")
        try:
            self.connect(self.broker)
        except:
            print(f"Cannot connect to broker: {self.broker}")
