import argparse
import requests


def print_basic_menu():
    print(f"1 - Pokaz opcje wyswietlania "
          f"\n2 - Pokaz opcje wlaczania punktow swietlnych "
          f"\n3 - Pokaz opcje wylaczania punktow swietlnych "
          f"\n4 - Pokaz stan polaczenia"
          f"\n5 - Usun urzadzenie z bazy danych "
          f"\n6 - Wyswietl ponownie opis menu "
          f"\n0 - Rozlacz i zakoncz dzialanie")


def show_lightbubs_menu(url, port):
    detailed_command = input("\t1 - Pokaz wszystkie"
                             "\n\t2 - Pokaz tylko wlaczone "
                             "\n\t3 - Pokaz tylko wylaczone "
                             "\n\t4 - Pokaz konkretny punkt swietlny "
                             "\n\t5 - Cofnij \n\t- ")
    if detailed_command == '1':
        print(requests.get(f'{url}:{port}/api/lightbulbs/all').text)
    elif detailed_command == '2':
        print(requests.get(f'{url}:{port}/api/lightbulbs/on').text)
    elif detailed_command == '3':
        print(requests.get(f'{url}:{port}/api/lightbulbs/off').text)
    elif detailed_command == '4':
        id_to_show = input("\t\tPodaj id punktu swietlnego: ")
        print(requests.get(f'{url}:{port}/api/lightbulbs/{id_to_show}').text)
    elif detailed_command == '5':
        return None


def turn_lightbubs_on_menu(url, port):
    detailed_command = input("\t1 - Wlacz wszystkie"
                             "\n\t2 - Wlacz konkretne urzadzenie"
                             "\n\t3 - Cofnij\n\t-")
    if detailed_command == '1':
        print(requests.post(f'{url}:{port}/api/lightbulbs/all', json={"condition": "ON"}).text)
    elif detailed_command == '2':
        turn_on_id = input("\t\tPodaj id punktu swietlnego: ")
        print(requests.post(f'{url}:{port}/api/lightbulbs/{turn_on_id}', json={"condition": "ON"}).text)
    elif detailed_command == '3':
        return None


def turn_lightbubs_off_menu(url, port):
    detailed_command = input("\t1 - Wylacz wszystkie"
                             "\n\t2 - Wylacz konkretne urzadzenie"
                             "\n\t3 - Cofnij\n\t-")
    if detailed_command == '1':
        print(requests.post(f'{url}:{port}/api/lightbulbs/all', json={"condition": "OFF"}).text)
    elif detailed_command == '2':
        turn_on_id = input("\tPodaj id punktu swietlnego: ")
        print(requests.post(f'{url}:{port}/api/lightbulbs/{turn_on_id}', json={"condition": "OFF"}).text)
    elif detailed_command == '3':
        return None


def delete_menu(url, port):
    detailed_command = input("\t1 - Usun wszystkie urzadzenia z bazy danych"
                             "\n\t2 - Usun wybrane urzadzenie z bazy danych"
                             "\n\t3 - Cofnij")
    if detailed_command == '1':
        print(requests.delete(f'{url}:{port}/api/lightbulbs/all').text)
    elif detailed_command == '2':
        delete_id = input("\t\tPodaj id punktu swietlnego: ")
        print(requests.delete(f'{url}:{port}/api/lightbulbs/{delete_id}').text)
    elif detailed_command == '3':
        return None


def show_interface(url, port):
    print_basic_menu()
    while True:
        user_input = input("- ").lower()
        if user_input == '1':
            show_lightbubs_menu(url, port)

        elif user_input == '2':
            turn_lightbubs_on_menu(url, port)

        elif user_input == '3':
            turn_lightbubs_off_menu(url, port)

        elif user_input == '4':
            print(f"Polaczenie z brokeren: {requests.get(f'{url}:{port}/api/connection').text}")

        elif user_input == '5':
            delete_menu(url, port)

        elif user_input == '6':
            print_basic_menu()

        elif user_input == '0':
            print(requests.delete(f'{url}:{port}/api/connection').text)
            break

        else:
            print("Nie rozpoznano polecenia")


def manage_arguments():
    parser = argparse.ArgumentParser('Konfiguracja klienta punktu swietlnego')
    parser.add_argument('-url', dest='flask_url', default='http://127.0.0.1',
                        help='Adres serwera REST API, domyslnie http://127.0.0.1', required=False)
    parser.add_argument('-p', dest='flask_port', default='5000',
                        help='Port serwera API, domyslnie 5000', required=False)

    return parser.parse_args()


if __name__ == '__main__':
    args = manage_arguments()
    show_interface(args.flask_url, args.flask_port)
