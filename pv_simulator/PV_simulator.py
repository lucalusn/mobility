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
from aio_pika import IncomingMessage
from json import loads
import asyncio


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
    def __init__(self,
                 broker: Broker,
                 max_pv: float,
                 delta_time: int,
                 out_folder: str=None) -> None:
        """
        :param broker: Broker obj
        :param max_pv: maximum power value
        :param delta_time: time between the creation of two consecutive messages
        :param out_folder: output folder where the data will be saved.
        """
        self.broker = broker
        self.address = broker.address
        self.queue_name = broker.queue_name
        self.max_pv_value = max_pv
        self.delay_time = delta_time

        # Set folder and filename
        self.folder = out_folder if out_folder is not None and path.isdir(out_folder)else str(Path.home())
        self.filename = path.join(self.folder,"result_"+datetime.now().strftime("%m_%d_%Y %H_%M_%S").replace(" ","_")+".txt")

        # create a value for each second of the day
        self.simulated_data =  [gauss(i, self.max_pv_value, 13, np.sqrt(6)) for i in np.linspace(0, 24, 24 * 60 * 60)]


    async def connect_to_broker(self):
        """
        Create a connection with the broker
        """
        await self.broker.connect()

    async def disconnect_to_broker(self):
        """
        close the connection with the broker
        """
        await self.broker.close()

    async def write_on_file(self,data:Dict):
        """
        :param data: values
        Save data to the file
        """
        if not path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("Timestamp \nMeter_value [kW]\nPV_value [kW]\nTot_value [kW]\n\n")
        df = DataFrame(columns=['Timestamp', "Meter_value", "PV_value", "Tot_value"])
        df.loc[0] = list(data.values())
        df.to_csv(self.filename, sep='\t', index=False, header=False, mode='a')


    async def process_message(self,msg:IncomingMessage)->None:
        """
        Callback function for receiving the message from the message queue
        The message is a dict with keys: 'Timestamp' and 'Meter_value'
        :param msg: message got from the queue
        """
        msg = loads(msg.body.decode('utf-8'))
        pv_value = self.simulated_data[ get_sec(t=msg['Timestamp']) ]
        data ={'Timestamp': msg['Timestamp'],
               'Meter_value': msg['Meter_value']/1000,
               'PV_value': pv_value,
               'Tot_value': pv_value + msg['Meter_value']/1000}
        await self.write_on_file(data=data)


    async def consume_data(self)->None:
        """
        Consumes the message
        """
        await self.broker.consume_msg(self.process_message)
        await asyncio.sleep(self.delay_time)