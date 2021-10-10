import unittest

from pv_simulator import arg_parser
import pathlib
from os import path
import argparse

CURRENT_DIR =pathlib.Path(__file__).parent.resolve()


class get_service_default_param_test(unittest.TestCase):
    def test_default_values(self):
        d0 = {
            "pv_max_power": 3400,
            "meter_max_power": 9000,
            "meter_min_power": 0,
            "output_folder": "",
            "delta_time": 5}
        self.assertDictEqual(arg_parser.get_service_default_param(),d0)


class get_cfg_rabbitMQ_test(unittest.TestCase):
    def test_file_not_found(self):
        self.assertDictEqual(arg_parser.get_cfg_rabbitMQ(f="not_exist.json"), dict())

    def test_invalid_file(self):
        self.assertDictEqual(arg_parser.get_cfg_rabbitMQ(f=path.join(CURRENT_DIR,"demo_invalid_cfg_rabbitMQ.json")), dict())

    def test_valid_file(self):
        d = {"address": "amqp://guest:guest@localhost:5672/","queue_name": "prova"}
        self.assertDictEqual(arg_parser.get_cfg_rabbitMQ(f=path.join(CURRENT_DIR,"demo_cfg_rabbitMQ.json")), d)


class get_cfg_services_test(unittest.TestCase):
    default_values = {
        "pv_max_power": 3400,
        "meter_max_power": 9000,
        "meter_min_power": 0,
        "output_folder": "",
        "delta_time": 5}
    def test_file_not_found(self):
        self.assertDictEqual(arg_parser.get_cfg_services(f="not_exist.json"), self.default_values)

    def test_miss_params_file(self):
        d = {
            "pv_max_power": 3000,
            "meter_max_power": 9000,
            "meter_min_power": 0,
            "output_folder": "",
            "delta_time": 2}
        self.assertDictEqual(arg_parser.get_cfg_services(f=path.join(CURRENT_DIR,"demo_miss_param_cfg_services.json")), d)

    def test_valid_file(self):
        d = {
          "pv_max_power": 3400,
          "meter_max_power": 9000,
          "meter_min_power": 0,
          "output_folder": "",
          "delta_time": 2}
        self.assertDictEqual(arg_parser.get_cfg_services(f=path.join(CURRENT_DIR,"demo_cfg_services.json")), d)


if __name__ == '__main__':
    unittest.main()
