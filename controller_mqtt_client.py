import paho.mqtt.client as mqtt
import time
from controller_sqlite_client import ControllerSqlite


class ControllerMQTT(mqtt.Client):
    def __init__(self, controller_name, database_name='lightbulbs', sql_table_name='lightbulbs'):
        super(ControllerMQTT, self).__init__(controller_name)
        self.connected_lightbulbs_list = []  # TODO przerobic na liste robiona z selecta do sqllite
        self.sql_client = ControllerSqlite(f"{database_name}.sqlite3")
        self.sql_client.connect_to_database()
        self.sql_client.create_table_if_dosent_exists(sql_table_name)

    def on_log(self, client, userdata, level, buf):
        # print(f"log {buf}") #TODO zapis logów do pliku
        pass

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subscribing to: [active, nonactive]")
        self.subscribe("active")
        self.subscribe("nonactive")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(f"Disconnected result code {str(rc)}")
        self.sql_client.delete_table()
        self.sql_client.sqlite_connection.close()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))

        if topic == 'active':
            # if m_decode not in self.connected_lightbulbs_list:
            print(f"New lighbulb detected, ID: {m_decode}")
            self.connected_lightbulbs_list.append(m_decode)
            new_topic_name = f"status-{m_decode}"
            print(f"Subscribing to {new_topic_name}")
            self.subscribe(new_topic_name)
            self.sql_client.add_lightbulb(m_decode, '?')

        elif 'status-' in topic:
            lighbulb_id = topic[7:]  # recznie usuwam 'status-', .strip moglby prowadzic do bugu gdyby id == 'status_'
            if m_decode == 'ON' or m_decode == 'OFF':
                self.sql_client.change_status_lightbulb(m_decode, lighbulb_id)
                print(f"Status of lighbulb {lighbulb_id} updated! New status: {m_decode}")

        elif topic == 'nonactive':
            last_status = self.sql_client.select_lightbulbs(f"where {self.sql_client.id_col_name} = '{m_decode}'")
            print(f"Lightbulb's interface {m_decode} is no longer active! Last known status was: {last_status}")
            self.delete_lightbulb_from_db(m_decode)

        # TODO dodac still active jesli starczy czasu
        else:
            print(f"message from topic - {topic}\nMessage: {m_decode}")

    def delete_lightbulb_from_db(self, lb_id):
        if lb_id not in self.connected_lightbulbs_list:
            print("Nie rozpoznano id urzadzenia!")
            return None
        self.sql_client.delete_lightbulb(lb_id)

    def show_lightbulbs(self, condition=""):
        if condition == "ON" or condition == "OFF":
            condition = f" where {self.sql_client.status_col_name} = '{condition}'"

        # jeśli istnieje warunek i nie dotyczy statusu, musi dotyczyć ID
        elif condition != "":
            if condition in self.connected_lightbulbs_list:
                condition = f" where {self.sql_client.id_col_name} = '{condition}'"
            else:
                print("Nie wykryto punktu swietlnego o podanym id!")
                return None

        print(self.sql_client.select_lightbulbs(condition))

    def change_lightbulbs_status(self, new_status, id=None):
        if id:
            self.publish(f"command-{id}", new_status, retain=True)
        else:
            self.publish("command-all", new_status, retain=True)
        self.sql_client.change_status_lightbulb(new_status, id)
        print("Poprawnie opublikowano status!")
