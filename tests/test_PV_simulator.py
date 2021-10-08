import unittest
from pv_simulator import PV_simulator
from datetime import datetime


class gauss_test(unittest.TestCase):
    def test_gauss(self):
        self.assertAlmostEqual(1.5966859,PV_simulator.gauss(x=10,A=3.4,mu=13,sigma=2.44),5)

class get_sec_test(unittest.TestCase):
    def test_get_sec(self):
        self.assertEqual(53759,PV_simulator.get_sec(datetime(year=2020, month=11, day=28, hour=14, minute=55, second=59).strftime("%m-%d-%Y %H_%M_%S")))
        self.assertEqual(0,PV_simulator.get_sec(datetime(year=2020, month=11, day=28, hour=0, minute=0, second=0).strftime("%m-%d-%Y %H_%M_%S")))


if __name__ == '__main__':
    unittest.main()
