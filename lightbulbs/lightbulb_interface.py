import time
import sys
sys.path.append('../')
from lightbulbs.lightbulb import LightBulb


def connect_to_broker(client):
    print(f"connecting to brokrer {client.broker}")
    try:
        client.connect(client.broker)
        client.loop_start()
    except:
        print(f"Cannot connect to broker: {client.broker}")

def main(*args, **kwargs):
    #TODO dodac __init__
    #TODO zrobic sprawdzanie zajetosci ID urzadzenia
    client = LightBulb("Alfa")

    connect_to_broker(client)
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
            connect_to_broker(client,broker)

        else:
            print("Command unknow")
    client.loop_stop()

if __name__ == "__main__":
    main()