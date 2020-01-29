import datetime
import paho.mqtt.client as mqtt
from controller_sqlite_client import ControllerSqlite


class ControllerMQTT(mqtt.Client):
    def __init__(self, controller_name, database_name,  log):
        super(ControllerMQTT, self).__init__(controller_name)
        self.connected_lightbulbs_list = []
        self.sql_client = ControllerSqlite(f"{database_name}.sqlite3")
        self.sql_client.connect_to_database()
        self.sql_client.create_table_if_dosent_exists('lightbulbs')
        self.log = log


    def on_log(self, client, userdata, level, buf):
        if self.log:
            with open("controller_logs.txt", 'a') as f:
                time_stamp = datetime.datetime.now()
                time_stamp = time_stamp.strftime("%d/%m/%Y %H:%M:%S")
                f.write(f"\n{time_stamp} LOG: {buf}")
        else:
            pass

    def on_connect(self, client, userdata, flags, rc):
        print(f"Subskrybowanie: [active, nonactive]")
        self.subscribe("active")
        self.subscribe("nonactive")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(f"Rozloczono z kodem: {str(rc)}")
        self.sql_client.delete_table()
        self.sql_client.sqlite_connection.close()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))

        if topic == 'active':
            self.connected_lightbulbs_list.append(m_decode)
            self.subscribe(f"status-{m_decode}")
            self.sql_client.add_lightbulb(m_decode, '?')
            print(f"Nowe urzadzenie wykryte, ID: {m_decode} "
                  f"\nSubskrybowanie: status - {m_decode}")

        elif 'status-' in topic:
            lighbulb_id = topic[7:]
            if m_decode == 'ON' or m_decode == 'OFF':
                self.sql_client.change_status_lightbulb(m_decode, lighbulb_id)
                print(f"Status urzadzenia {lighbulb_id} "
                      f"zaktualizowany! Nowy status: {m_decode}")

        elif topic == 'nonactive':
            last_status = self.sql_client.select_lightbulbs(f"where {self.sql_client.id_col_name} = '{m_decode}'")
            print(f"Urzadzenie {m_decode} nie jest juz aktywne! Ostatni znany status to: {last_status}")
            self.delete_lightbulb_from_db(m_decode)

        else:
            print(f"Wiadomosc z tematu - {topic}\nWiadomosc: {m_decode}")

    def delete_lightbulb_from_db(self, lb_id):
        if lb_id not in self.connected_lightbulbs_list:
            print(f"Nie rozpoznano ID urzadzenia!")
            return None
        self.sql_client.delete_lightbulb(lb_id)

    def show_lightbulbs(self, condition=""):
        if condition == "ON" or condition == "OFF":
            condition = f" where {self.sql_client.status_col_name} = '{condition}'"

        elif condition != "":
            if condition in self.connected_lightbulbs_list:
                condition = f" where {self.sql_client.id_col_name} = '{condition}'"
            else:
                print(f"Nie wykryto punktu swietlnego o podanym id!")
                return None

        return self.sql_client.select_lightbulbs(condition)

    def change_lightbulbs_status(self, new_status, id=None):
        if id:
            self.publish(f"command-{id}", new_status, retain=True)
        else:
            self.publish("command-all", new_status, retain=True)
        print(f"Poprawnie opublikowano status!")
