import time
import sys
sys.path.append('../')
from lightbulbs.lightbulb import LightBulb


def connect_to_broker(client):
    print(f"connecting to brokrer {client.broker}")
    try:
        client.connect(client.broker)
    except:
        print(f"Cannot connect to broker: {client.broker}")

def main(*args, **kwargs):
    #TODO zrobic sprawdzanie zajetosci ID urzadzenia
    #TODO arg_parser
    client = LightBulb("Beta")

    connect_to_broker(client)
    client.loop_start()
    time.sleep(0.5)
    print(f"Lightb {client.id}\nConnected: {client.is_connected()}\n{client.show_current_status()}")
    print("To show current status: type 'status', turning on/off type 'on' or 'off', to exit type 'e' ", end="")
    print("for connection checking: 'connected' or 'c', to reconnect 'reconnect' or 'r'")
    while True:
        x = input("- ").lower()
        if x == 'status' or x=='s':
            print(client.show_current_status())
        elif x == 'on':
            client.change_status(1)
        elif x == 'off':
            client.change_status(0)
        elif x == 'exit' or x =='e':
            client.disconnect()
            break
        elif x == 'connected' or x == 'c':
            print(f"Connected: {client.is_connected()}")
        elif x == 'reconnect' or x == 'r':
            connect_to_broker(client.broker)
        elif x == '0':
            client.on_disconnect()
            break
        else:
            print("Command unknow")
    client.loop_stop()
    client.disconnect()# mozna uzyc publish single ale jest mniej czytelne wg mnie.

if __name__ == "__main__":
    main()