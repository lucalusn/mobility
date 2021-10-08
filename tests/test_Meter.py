import unittest

from pv_simulator import Meter



class dummy_test(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(Meter.dummy_broker())



if __name__ == '__main__':
    unittest.main()
