"""
The Meter produces messages to the broker with random but continuous values from 0 to 9000 Watts.
This is to mock a regular home power consumption
"""

import asyncio
from pv_simulator.Broker import Broker
from numpy import random
from datetime import datetime
from json import dumps

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

    async def open_connection(self)->None:
        """
        Open the connection with the Broker
        """
        await self.broker.connect()

    async def close_connection(self)->None:
        """
        close the connection to the Broker
        """
        await self.broker.close()

    async def send_messages(self)->None:
        """
        Continuously sends messages to the Broker
        """
        while True:
            msg = {"Timestamp":datetime.now().strftime("%m-%d-%Y %H_%M_%S"),
                   "Meter_value": random.uniform(self.min_power, self.max_power)}
            try:
                await self.broker.publish_msg(dumps(msg))
                await asyncio.sleep(self.delta_time)
            except Exception as e:
                print(f"Not enable to publish message '{msg}' because '{e}' exception")
                raise e
