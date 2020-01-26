import paho.mqtt.client as mqtt


class LightBulb(mqtt.Client):
    def __init__(self,id, broker, stan):
        super(LightBulb, self).__init__(id)
        self._id = id # zakladam ze bedzie tekstem, w budynku lb raczej bd nazwane "front-1" || "portiernia"
        self._stan = stan #0:OFF 1:ON
        self.broker = broker
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
        self.publish(f"status-{self.id}", f'{self.stan}', retain=True)
        print(f"Status changed to: {self.stan}")

    def on_disconnect(self):
        self.publish("nonactive", self.id) #TODO dodać usuwanie na disconnecta w tablicy sql
        print("Succesfully disconnected")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        print("\nMessage from broker recived: ", end="")
        print(topic)
        if topic == f"command-{client.id}" or topic == "command-all":
            if m_decode == "ON" or m_decode == '1':
                self.change_status(1)
            elif m_decode == "OFF" or m_decode == '0':
                self.change_status(0)
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")

    def on_log(self, client, userdata, level, buf):
        #print(f"log {buf}")
        pass

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subscribing to: command-{self.id} and command-all")
        self.subscribe(f"command-{self.id}")
        self.subscribe("command-all")
        self.publish("active", self.id, retain=True)
        self.publish(f"status-{self.id}", f'{self.stan}', retain=True)

