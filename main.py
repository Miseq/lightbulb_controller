from controller_mqtt_client import ControllerMQTT
import time
import argparse
from controller_sqlite_client import ControllerSqlite

def print_menu():
    print("1 - Pokaz opcje wyswietlania \n2 - Pokaz opcje wlaczania punktow swietlnych "
          "\n3 - Pokaz opcje wylaczania punktow swietlnych \n4 - Pokaz stan polaczenia "
          "\n5 - Wyswietl ponownie opis menu \n0 - Rozlacz i zakoncz dzialanie")

def show_interface(controller):
    print_menu()
    while True:
        user_input = input("- ").lower()
        if user_input == '1':
            detailed_command = input("\t1 - Pokaz wszystkie"
                                     "\n\t2 - Pokaz tylko wlaczone "
                                     "\n\t3 - Pokaz tylko wylaczone "
                                     "\n\t4 - Pokaz konkretny punkt swietlny "
                                     "\n\t5 - Cofnij \n\t- ")
            if detailed_command == '1':
                controller.show_lightbulbs()
            elif detailed_command == '2':
                controller.show_lightbulbs("ON")
            elif detailed_command == '3':
                controller.show_lightbulbs("OFF")
            elif detailed_command == '4':
                id_to_show = input("\t\tPodaj id punktu swietlnego: ")
                controller.show_lightbulbs(id_to_show)
            elif detailed_command == '5':
                continue

        elif user_input == '2':
            detailed_command = input("\t1 - Wlacz wszystkie"
                                     "\n\t2 - Wlacz konkretne urzadzenie"
                                     "\n\t3 - Cofnij")
            if detailed_command == '1':
                controller.change_lightbulbs_status('ON')
            elif detailed_command =='2':
                turn_on_id = input("\t\tPodaj id punktu swietlnego: ")
                controller.change_lightbulbs_status('ON', turn_on_id)
            elif detailed_command == '3':
                continue

        elif user_input == '3':
            detailed_command = input("\t1 - Wylacz wszystkie"
                                     "\n\t2 - Wylacz konkretne urzadzenie"
                                     "\n\t3 - Cofnij\n-")
            if detailed_command == '1':
                controller.change_lightbulbs_status('OFF')
            elif detailed_command =='2':
                turn_on_id = input("\tPodaj id punktu swietlnego: ")
                controller.change_lightbulbs_status('OFF', turn_on_id)
            elif detailed_command == '3':
                continue
            else:
                print("nie rozpoznano komendy!")

        elif user_input == '4':
            print(f"Polaczenie z brokeren: {controller.is_connected()}")

        elif user_input == '5':
            print_menu()
        elif user_input == '0':
            break
        else:
            print("Nie rozpoznano polecenia!")

def main():
    controller = ControllerMQTT(controller_name="Controller")

    print(f"connecting to brokrer {controller.broker}")
    #TODO argumenty, help, adres, port, set_all, log itp.

    controller.connect('localhost') # TODO zrobic na argumencie
    controller.loop_start()
    controller.subscribe("id")
    time.sleep(0.5)

    show_interface(controller)

    controller.loop_stop()
    controller.disconnect()

if __name__ == '__main__':
    main()