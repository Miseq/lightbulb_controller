import time
import unittest
import sys
sys.path.append('../')
from controller_mqtt_client import ControllerMQTT


# Dosłownie co drugie uruchomienie dziala, wyrzuca blad, ze database jest zablokowana, nie zdazylem zdebuowac
class TestControllerMQTT(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestControllerMQTT, self).__init__(*args, **kwargs)
        self.test_controller = ControllerMQTT('test', 'test_controller', 'test')

    def test_on_message_active(self):
        self.test_controller.connect('localhost')
        self.test_controller.loop_start()
        self.test_controller.subscribe('active_test')
        self.test_controller.publish('active_test', 'TEST')
        time.sleep(0.5)
        self.test_controller.loop_stop()
        assert 'TEST' in self.test_controller.connected_lightbulbs_list

    def test_on_message_status(self):
        self.test_controller.connect('localhost')
        self.test_controller.loop_start()
        self.test_controller.publish('status-TEST', 'ON', retain=True)
        time.sleep(0.5)
        self.test_controller.loop_stop()
        output = self.test_controller.sql_client.select_lightbulbs('TEST')
        assert output[0][1] == 'ON'

    def test_on_message_nonactive(self):
        self.test_controller.connect('localhost')
        self.test_controller.loop_start()
        self.test_controller.subscribe('nonactive')
        self.test_controller.publish('nonactive', 'TEST',)
        time.sleep(0.5)
        self.test_controller.loop_stop()
        output = self.test_controller.sql_client.select_lightbulbs("")
        print(output)
        assert output == []


if __name__ == '__main__':
    unittest.main()
