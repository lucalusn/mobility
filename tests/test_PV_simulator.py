import unittest

from pv_simulator import PV_simulator



class dummy_test(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(PV_simulator.dummy_broker())



if __name__ == '__main__':
    unittest.main()
