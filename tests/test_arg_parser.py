import unittest

from pv_simulator import arg_parser


class get_service_default_param_test(unittest.TestCase):
    def test_default_values(self):
        d = {
            "pv_max_power": 3400,
            "meter_max_power": 9000,
            "meter_min_power": 0,
            "output_folder": "",
            "frequency": 5}
        self.assertDictEqual(arg_parser.get_service_default_param(),d)



if __name__ == '__main__':
    unittest.main()
