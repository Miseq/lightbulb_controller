import unittest
from lightbulbs.lightbulbs import LightBulb

class MyTestCase(unittest.TestCase):
    def __init__(self):
        super(MyTestCase, self).__init__()
        self.test_lighbulb = LightBulb(port=8080)

    def test_turn_on(self):
        """
        Testing if turing on is working
        """
        self.test_lighbulb.status = 0
        self.test_lighbulb.turn_on()
        assert self.test_lighbulb.status == 1

    def test_turn_off(self):
        """
        Testing if turning off is working
        :return:
        """
        self.test_lighbulb.status = 1
        self.test_lighbulb.turn_off()
        assert self.test_lighbulb.status == 0

    def test_get_status(self):
        """
        Testing lighbulb's response about it's status
        :return:
        """
        assert self.test_lighbulb.get_status() == self.test_lighbulb.status


if __name__ == '__main__':
    unittest.main()
