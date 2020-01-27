from controller_mqtt_client import ControllerMQTT
import time
import argparse


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
            elif detailed_command == '2':
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
            elif detailed_command == '2':
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


def manage_arguments():
    parser = argparse.ArgumentParser('Konfiguracja klienta punktu swietlnego')
    # parser.add_help ???
    parser.add_argument('-n', dest='name', help='Unikatowa nazwa controllera', required=True)
    parser.add_argument('-b', dest='broker', default='localhost',
                        help='Opcjonalny adres brokera, domyslnie localhost', required=False)
    parser.add_argument('-db', dest='database', default='lightbulbs',
                        help='Nazwa uzywanej bazy danych, domyslnie "lighbulbs"', required=False)
    parser.add_argument('-p', dest='port', default='1883',  help='Port laczycy z brokerem"', required=False)
    parser.add_argument('-l', dest='log', default='True',
                        help='Okresla czy program zapisuje logi komunikacji przez mqtt', required=False)
    return parser.parse_args()


def main():
    args = manage_arguments()
    controller = ControllerMQTT(controller_name=args.name, database_name=args.database, log=args.log)

    print(f"connecting to brokrer {args.broker}")
    controller.connect(args.broker)
    controller.loop_start()
    time.sleep(0.5)
    show_interface(controller)
    controller.loop_stop()
    controller.disconnect()


if __name__ == '__main__':
    main()
