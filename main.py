import paho.mqtt.client as mqtt
import time
def main():
    broker='localhost'
    client = mqtt.Client("Controller")
    print(f"connecting to brokrer {broker}")

    client.connect(broker)
    client.loop_start()
    client.subscribe("id")
    time.sleep(2)

    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()