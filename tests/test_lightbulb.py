import time
import unittest
import sys

sys.path.append('../')
from lightbulbs.lightbulb import LightBulb


class TestLightBulb(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLightBulb, self).__init__(*args, **kwargs)
        self.test_lb = LightBulb('test', 'localhost', 'OFF')

    def test_id(self):
        self.assertEqual(self.test_lb.id, 'test')

    def test_status(self):
        self.assertEqual(self.test_lb.status, 'OFF')

    def test_connect_to_broker(self):
        self.test_lb.connect_to_broker()
        self.test_lb.loop_start()
        time.sleep(0.5)
        connetion = self.test_lb.is_connected()
        self.test_lb.loop_stop()
        assert connetion is True

    def test_change_status(self):
        self.test_lb.change_status('ON')
        self.assertEqual(self.test_lb.status, 'ON')

    def test_on_message_command_id(self):
        self.test_lb.connect_to_broker()
        self.test_lb.loop_start()
        self.test_lb.subscribe(f'command-{self.test_lb.id}')
        self.test_lb.publish(f'command-{self.test_lb.id}', 'OFF')
        time.sleep(0.5)
        self.test_lb.loop_stop()
        self.assertEqual(self.test_lb.status, 'OFF')

    def test_on_message_command_all(self):
        self.test_lb.connect_to_broker()
        self.test_lb.loop_start()
        self.test_lb.subscribe('command-all')
        self.test_lb.publish(f'command-all', 'ON')
        time.sleep(0.5)
        self.test_lb.loop_stop()
        self.assertEqual(self.test_lb.status, 'ON')


if __name__ == '__main__':
    unittest.main()
