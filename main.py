from controller_mqtt_client import ControllerMQTT
import time

def main():
    broker='localhost'
    controller = ControllerMQTT("Controller")
    print(f"connecting to brokrer {broker}")

    controller.connect(broker)
    controller.loop_start()
    controller.subscribe("id")
    while True:
        x = input("- ").lower()
        if x == 'status' or x=='s':
            print(controller.show_current_status())


        elif x == 'connected' or x == 'c':
            print(f"Connected: {controller.is_connected()}")
    time.sleep(0.5)
    print("@")


if __name__ == '__main__':
    main()