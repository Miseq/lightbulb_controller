import time
from lightbulbs.lightbulb import LightBulb

def main(*args, **kwargs):
    broker='localhost'
    client = LightBulb("Alfa")

    print(f"connecting to brokrer {broker}")
    client.connect(broker)
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
            client.reconnect()
            time.sleep(0.5)
            print(f"Reconnected: {client.is_connected()}")
        else:
            print("Command unknow")
    client.loop_stop()



if __name__ == '__main__':
    main()