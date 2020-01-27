import datetime
import paho.mqtt.client as mqtt


class LightBulb(mqtt.Client):
    def __init__(self, id, broker, status, log):
        super(LightBulb, self).__init__(id)
        self._id = id  # zakladam ze bedzie tekstem, w budynku lb raczej bd nazwane "front-1" || "portiernia"
        self._status = status
        self.broker = broker
        self.log = log

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status != 'ON' and new_status != 'OFF':
            raise ValueError("Niepoprawny status! Poprawne wartosci to 'ON' lub 'OFF'")
        self._status = new_status

    def on_log(self, client, userdata, level, buf):
        if self.log:
            with open(f"./logs/{self.id}.txt", 'a') as f:
                time_stamp = datetime.datetime.now()
                time_stamp = time_stamp.strftime("%d/%m/%Y %H:%M:%S")
                f.write(f"\n{time_stamp} LOG: {buf}")
        else:
            pass

    def show_current_status(self):
        return f"Status:{self.status}"

    def change_status(self, new_status):
        self.status = new_status
        self.publish(f"status-{self.id}", f'{self.status}', retain=True)
        print(f"Status zmieniony na: {self.status}")

    def on_disconnect(self):
        self.publish("nonactive", self.id)
        print("Poprawnie rozlaczono")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print(f"\nOtrzymano wiadomosc na temat: {topic}")
        print(topic)
        if topic == f"command-{client.id}" or topic == "command-all":
            if m_decode == "ON":
                self.change_status('ON')
            elif m_decode == "OFF":
                self.change_status('OFF')
        else:
            print(f"\nWiadomosc: {m_decode}")

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subskrybowane tematy: 'command-{self.id}' oraz 'command-all'")
        self.subscribe(f"command-{self.id}")
        self.subscribe("command-all")
        self.publish("active", self.id, retain=True)
        self.publish(f"status-{self.id}", f'{self.status}', retain=True)

    def connect_to_broker(self):
        print(f"Polaczono z brokerem: {self.broker}")
        try:
            self.connect(self.broker)
        except:
            print(f"Nie udalo sie nawiazac polaczenia z brokerem: {self.broker}")
