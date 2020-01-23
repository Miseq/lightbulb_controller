import paho.mqtt.client as mqtt
import time
def main():
    broker='localhost'
    client = mqtt.Client("Controller")
    print(f"connecting to brokrer {broker}")

    client.connect(broker)
    client.loop_start()
    client.subscribe("id")
    client.publish("command-all", "1")
    time.sleep(0.5)
    print("@")


if __name__ == '__main__':
    main()