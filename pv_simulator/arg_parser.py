"""
Parser used for collecting the user input files, checking the validity of the files and eventually fill the missing values with the defaults value

example of cfg_rabbitMQ.json:  It is mandatory
{
  "address": "amqp://guest:guest@localhost:5672/",
  "queue_name": "prova"
}

example of cfg_services.json:   if it miss the script will use the following values
{
  "pv_max_power": 3400,
  "meter_max_power": 9000,
  "meter_min_power": 0,
  "output_folder": "",
  "frequency": 2
}

"""

import argparse
from typing import Dict,Union
from json import load
from os import path

# default values, used in case of missing 'services_param' json file
PV_MAX_POWER = 3400
METER_MAX_POWER = 9000
METER_MIN_POWER = 0
OUTPUT_FOLDER = ""
FREQUENCY = 5

def create_parser():
    """
    Create the parser
    """
    parser = argparse.ArgumentParser(description="System that collects every 'n' seconds data from a Meter, which generates random values between 0-9kW for mocking a regular home power consumption, generates simulated PV (photovoltaic) power values (in kW) and write these results on file")
    parser.add_argument("-c", "--config_rabbitMQ", help="json file containing queue access parameters", required=True)
    parser.add_argument("-v", "--services_param", help="json file containing values for the services")
    return parser

def get_service_default_param()->Dict:
    """
    In case the service_param arg is not filled it load these default params
    :return: params of the services
    """
    return {
            "pv_max_power": PV_MAX_POWER,
            "meter_max_power": METER_MAX_POWER,
            "meter_min_power": METER_MIN_POWER,
            "output_folder": OUTPUT_FOLDER,
            "frequency": FREQUENCY }

def get_cfg_rabbitMQ(f:str)->Dict:
    """
    Check if the 'rabbitMQ' config file is valid and returns the values
    :param f: path to the cfg file
    :return: params
    """
    if path.isfile(f):
        with open(f, 'r') as cfg:
            par = {k.lower():v for k,v in load(cfg).items()}
            if "address" in par.keys() and "queue_name" in par.keys():
                return par
            else:
                print("ERROR: invalid 'config_rabbitMQ' file. It does not contain 'address' and/or 'queue_name' field(s)")
    print("ERROR: file not found")
    return dict()


def get_cfg_services(f:Union[str, None])->Dict:
    """
    Check if the 'services' config file is valid and returns the values
    :param f: path to the cfg file
    :return: params
    """
    if path.isfile(f):
        with open(f, 'r') as cfg:
            par = {k.lower():v for k,v in load(cfg).items()}
            for p,v in get_service_default_param().items():
                if p not in par.keys():
                    par.update({p:v})
            return par
    return get_service_default_param()
