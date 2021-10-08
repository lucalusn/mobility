"""
It listens to the broker for the meter values, generate a simulated PV power value and adds this value to the meter value and output the result.
The result saved on file have the following informations:
    -) timestamp
    -) meter power value
    -) PVpower value
    -) sum of the powers (meter + PV)).
"""
from os import path
import numpy as np
from datetime import datetime
from pv_simulator.Broker import Broker

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
                 min_pv: float,
                 max_pv: float,
                 delta_time: int,
                 out_folder: str="") -> None:
        """
        :param address: address of a broker (e.g: 'localhost' or IP address)
        :param queue_name: Name of the rabbitMQ queue
        :param broker: Broker obj
        :param min_pv: minimum power value
        :param max_pv: maximum power value
        :param delta_time: time between the creation of two consecutive messages
        :param out_folder: output folder where the data will be saved.
        """
        self.address = address
        self.queue_name = queue_name
        self.broker = broker
        self.min_pv_value = min_pv
        self.max_pv_value = max_pv
        self.folder = out_folder
        self.delay_time = delta_time
        self.filename = datetime.now().strftime("%m_%d_%Y %H_%M_%S").replace(" ","_")


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

    def write_on_file(self):
        """
        Save data to the file
        """
        pass

    def process_message(self,msg:str)->None:
        """
        Callback function for receiving the message from the message queue
        :param msg: message got from the queue
        """
        pass