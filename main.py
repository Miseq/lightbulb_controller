from controller_mqtt_client import ControllerMQTT
import time

def main():
    broker='localhost'
    controller = ControllerMQTT("Controller")
    print(f"connecting to brokrer {broker}")

    controller.connect(broker)
    controller.loop_start()
    controller.subscribe("id")
    time.sleep(0.5)
    while True:
        x = input("- ").lower()
        if x == 'status' or x=='s':
            print(controller.dict_of_states)
            print(controller.connected_lightbulbs_list)

        elif x == 'connected' or x == 'c':
            print(f"Connected: {controller.is_connected()}")
        elif x == 'exit' or x=='e':
            break
    controller.loop_stop()
    print("naprawde chce ta prace :)")

if __name__ == '__main__':
    main()