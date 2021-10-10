"""
The Meter produces messages to the broker with random but continuous values from 0 to 9000 Watts.
This is to mock a regular home power consumption
"""

import asyncio
from pv_simulator.Broker import Broker
from numpy import random
from datetime import datetime
from json import dumps
from logging import Logger

class Meter:
    def __init__(self, min_power:float, max_power:float, delta_time: int, broker:Broker, logger:Logger=None)->None:
        """
        :param min_power: minimum power value
        :param max_power: maximum power value
        :param delta_time: time between the creation of two consecutive messages
        :param broker: Broker obj
        :param logger: logger obj
        """
        self.min_power = min_power
        self.max_power = max_power
        self.delta_time = delta_time
        self.broker = broker
        self.logger = logger

    async def open_connection(self)->None:
        """
        Open the connection with the Broker
        """
        self.logger.info("Meter trying to connect to broker")
        await self.broker.connect()

    async def close_connection(self)->None:
        """
        close the connection to the Broker
        """
        self.logger.info("Meter trying to disconnect to broker")
        await self.broker.close()

    async def send_messages(self, only_one:bool = False)->None:
        """
        :param only_one: Flag to send only one message
        Continuously sends messages to the Broker
        """
        while True:
            msg = {'Timestamp':str(datetime.now().strftime("%m-%d-%Y %H_%M_%S")),
                   'Meter_value': random.uniform(self.min_power, self.max_power)}
            try:
                await self.broker.publish_msg(dumps(msg))
                await asyncio.sleep(self.delta_time)
            except Exception as e:
                self.logger.error(f"PV_simulator not enable to publish message '{msg}' because '{e}' exception")
                raise e
            if only_one:
                break
