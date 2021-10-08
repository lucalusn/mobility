"""
The Meter produces messages to the broker with random but continuous values from 0 to 9000 Watts.
This is to mock a regular home power consumption
"""

from pv_simulator.Broker import Broker
from numpy import random
from datetime import datetime

class Meter:
    def __init__(self, min_power:float, max_power:float, delta_time: int, broker:Broker)->None:
        """
        :param min_power: minimum power value
        :param max_power: maximum power value
        :param delta_time: time between the creation of two consecutive messages
        :param broker: Broker obj
        """
        self.min_power = min_power
        self.max_power = max_power
        self.delta_time = delta_time
        self.broker = broker

    def open_connection(self)->None:
        """
        Enable the connection to the Broker
        """
        pass

    def close_connection(self)->None:
        """
        close the connection to the Broker
        """
        pass

    def send_messages(self)->None:
        """
        Continuously sends messages to the Broker
        """
        while True:
            msg = {datetime.now().strftime("%m-%d-%Y %H_%M_%S"):random.uniform(self.min_power, self.max_power)}