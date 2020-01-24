import paho.mqtt.client as mqtt
import time

class ControllerMQTT(mqtt.Client):
    def __init__(self, controller_name):
        super(ControllerMQTT, self).__init__(controller_name)
        self.connected_lightbulbs_list = []
        self.dict_of_states = {}

    def update_dict_of_states(self, lightbulb_id, lightbulb_status):
        self.dict_of_states[lightbulb_id] = lightbulb_status

    def on_log(self, client, userdata, level, buf):
        #print(f"log {buf}")
        pass

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subscribing to: active")
        self.subscribe("active")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(f"Disconnected result code {str(rc)}")
    

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        if topic == 'active':
            if m_decode not in self.connected_lightbulbs_list:
                print(f"New lighbulb detected, ID: {m_decode}")
                self.connected_lightbulbs_list.append(m_decode)

                new_topic_name = f"status-{m_decode}"
                print(f"Subscribing to {new_topic_name}")
                self.subscribe(new_topic_name)
                self.update_dict_of_states(m_decode, '?')

        elif 'status-' in topic:
            lighbulb_id = topic[7:]  # recznie usuwam 'status-', .strip moglby prowadzic do bugu gdyby id mialo status
            if m_decode == '1' or m_decode == '0':
                self.update_dict_of_states(lighbulb_id, m_decode)
                print(f"Status of lighbulb {lighbulb_id} updated! New status: {m_decode}")
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")