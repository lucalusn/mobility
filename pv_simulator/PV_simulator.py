"""
It listens to the broker for the meter values, generate a simulated PV power value and adds this value to the meter value and output the result.
The result saved on file have the following information:
    -) timestamp
    -) meter power value
    -) PVpower value
    -) sum of the powers (meter + PV)).
"""
from os import path
from pathlib import Path
import numpy as np
from datetime import datetime
from pv_simulator.Broker import Broker
from typing import Dict
from pandas import DataFrame


def get_sec(t)->int:
    """
    transform the given datatime in seconds elapsed in the day
    :param t: time in datatime (%m-%d-%Y %H:%M:%S)'s format
    :return: seconds elapsed in the day
    """
    h_min_sec=t.split(" ")[1].split("_")
    return int(h_min_sec[0])*3600 + int(h_min_sec[1])*60 + int(h_min_sec[2])

def gauss(x:float, A:float, mu:float, sigma:float)->float:
    """
    Return the value of a gaussian function in the point x
    :param x: point where the value will be calculated
    :param A: height of the curve's peak
    :param mu: position of the center of the peak
    :param sigma: standard deviation
    :return:
    """
    return A * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


class PV_simulator:
    def __init__(self, address: str,
                 queue_name: str,
                 broker: Broker,
                 max_pv: float,
                 delta_time: int,
                 out_folder: str="") -> None:
        """
        :param address: address of a broker (e.g: 'localhost' or IP address)
        :param queue_name: Name of the rabbitMQ queue
        :param broker: Broker obj
        :param max_pv: maximum power value
        :param delta_time: time between the creation of two consecutive messages
        :param out_folder: output folder where the data will be saved.
        """
        self.address = address
        self.queue_name = queue_name
        self.broker = broker
        self.max_pv_value = max_pv
        self.delay_time = delta_time

        # Set folder and filename
        self.folder = out_folder if out_folder is not None and path.isdir(out_folder)else str(Path.home())
        self.filename = "result_"+datetime.now().strftime("%m_%d_%Y %H_%M_%S").replace(" ","_")+".txt"

        # create a value for each second of the day
        self.simulated_data =  [gauss(i, self.max_pv_value, 13, np.sqrt(6)) for i in np.linspace(0, 24, 24 * 60 * 60)]


    def connect_to_broker(self):
        """
        Create a connection with the broker
        """
        self.broker.connect()

    def disconnect_to_broker(self):
        """
        close the connection with the broker
        """
        self.broker.close()

    def write_on_file(self,data:Dict):
        """
        :param data: values
        Save data to the file
        """
        if not path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("Timestamp\nMeter_value\nPV_value\nCombined_Value\n\n")
        df = DataFrame(columns=['Timestamp', "Meter_value", "PV_value", "Combined_Value"])
        df.loc[0] = list(data.values())
        df.to_csv(self.filename, sep='\t', index=False, header=False, mode='a')


    def process_message(self,msg:str)->None:
        """
        Callback function for receiving the message from the message queue
        :param msg: message got from the queue
        """
        # todo get the message and call write_on_file
        data ={"time_stamp":datetime.now(), "meter":0, "PV":0, "tot":0}
        self.write_on_file(data=data)