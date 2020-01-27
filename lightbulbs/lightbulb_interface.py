import time
import sys
sys.path.append('../')
from lightbulbs.lightbulb import LightBulb
import argparse




def print_menu():
    print("Interfejs punktu swietlnego: \n1-Wyswietl status \n2-Wlacz swiatlo \n3-Wylacz swiatlo "
          "\n4-Odnow polaczenie \n5-Wyswietl ponownie menu \n0-Rozlacz i zakoncz dzialanie programu")


def show_user_interface(client):
    print_menu()
    while True:
        x = input("- ").lower()
        if x == '1':
            print(f"Lightb {client.id}\nConnected: {client.is_connected()}\n{client.show_current_status()}")
        elif x == '2':
            client.change_status('ON')
        elif x == '3':
            client.change_status('OFF')
        elif x == '4':
            client.connect_to_broker()
        elif x == '5':
            print_menu()
        elif x == '0':
            client.disconnect()
            break
        else:
            print("Nieznana komenda")

def manage_arguments():
    parser = argparse.ArgumentParser('Konfiguracja klienta punktu swietlnego')
    #parser.add_help ???
    parser.add_argument('-id', dest='id',  help='Unikatowe ID clienta', required= True)
    parser.add_argument('-broker', dest='broker', default='localhost',
                        help='Opcjonalny adres brokera, domyslnie localhost', required=False)
    parser.add_argument('-status', dest='status', default='OFF',
                        help='Stan poczatkowy punktu swietlnego: ON/OFF', required=False )
    return parser.parse_args()

def main(*args, **kwargs):
    args = manage_arguments()
    client = LightBulb(args.id, args.broker, args.status)

    client.connect_to_broker()
    client.loop_start()
    time.sleep(0.5) # czas na poprawne pobranie i wyslanie wiadomosci
    
    show_user_interface(client)

    client.loop_stop()
    client.disconnect()# mozna uzyc publish single ale jest mniej czytelne wg mnie.

if __name__ == "__main__":
    main()