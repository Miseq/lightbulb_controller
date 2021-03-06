import argparse
import sys
import time

sys.path.append('../')
from lightbulb import LightBulb
#from lightbulbs.lightbulb import LightBulb # moze wymagac poprawy, zaleznie od sposobu uruchamiania
# jesli uruchamiamy przez IDE (PyCharm - zostawic bez zmian) jesli konosolowo z folderu nalezy zminic


def print_menu():
    print("Interfejs punktu swietlnego: "
          "\n1-Wyswietl status "
          "\n2-Wlacz swiatlo "
          "\n3-Wylacz swiatlo "
          "\n4-Odnow polaczenie "
          "\n5-Wyswietl ponownie menu "
          "\n6-Rozlacz i zakoncz dzialanie programu")


def show_user_interface(client):
    print_menu()
    while True:
        user_input = input("- ").lower()
        if user_input == '1':
            print(f"Lightb {client.id}\nConnected: {client.is_connected()}\n{client.status}")
        elif user_input == '2':
            client.change_status('ON')
        elif user_input == '3':
            client.change_status('OFF')
        elif user_input == '4':
            client.connect_to_broker()
        elif user_input == '5':
            print_menu()
        elif user_input == '0':
            client.disconnect()
            break
        else:
            print("Nieznana komenda")


def manage_arguments():
    parser = argparse.ArgumentParser('Konfiguracja klienta punktu swietlnego')
    # parser.add_help ???
    parser.add_argument('-id', dest='id', help='Unikatowe ID clienta', required=True)
    parser.add_argument('-broker', dest='broker', default='broker.hivemq.com',
                        help='Opcjonalny adres brokera, domyslnie localhost', required=False)
    parser.add_argument('-status', dest='status', default='OFF',
                        help='Stan poczatkowy punktu swietlnego: ON/OFF', required=False)
    parser.add_argument('-l', dest='log', default='True',
                        help='Okresla czy program zapisuje logi komunikacji przez mqtt"', required=False)
    return parser.parse_args()


def main():
    args = manage_arguments()
    client = LightBulb(args.id, args.broker, args.status, args.log)

    client.connect_to_broker()
    client.loop_start()
    time.sleep(0.5)  # czas na poprawne pobranie i wyslanie wiadomosci
    print(f"Lightb {client.id}\nConnected: {client.is_connected()}\n{client.status}")
    show_user_interface(client)

    client.loop_stop()
    client.disconnect()  # mozna uzyc publish single ale jest mniej czytelne wg mnie.


if __name__ == "__main__":
    main()
