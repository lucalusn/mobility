"""
Is a message-queueing, a rabbitMQ, that allows 'Meter' and 'PV_simulator' to communicate with each other.
It receives messages from 'Meter' and sends them to 'PV_simulator'
"""
import aio_pika
from typing import Callable

from logging import Logger

class Broker:
    def __init__(self,address: str, queue_name:str, logger:Logger=None)->None:
        """
        :param address: address of a broker (e.g: 'localhost' or IP address)
        :param queue_name: Name of the rabbitMQ queue
        :param logger: logger obj
        """
        self.address = address
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.message_queue = None
        self.logger=logger

    async def connect(self)->bool:
        """
        Create the connection and declare the queue
        In case it is not possible to create the connection an error message will explain the reason
        """
        try:
            self.connection = await aio_pika.connect(self.address)
            self.channel = await self.connection.channel()
            self.message_queue = await self.channel.declare_queue(self.queue_name)

            self.logger.info("broker connected")
        except Exception as e:
            self.logger.error (f"Not enable to create the connection because '{e}' exception")
            raise e
        return True

    async def close(self)->bool:
        """
        Closes the connection between Meter and PV_simulator
        In case it is not possible to close the connection an error message will explain the reason
        """
        if self.connection:
            try:
                await self.connection.close()
                self.logger.info("broker closed")
                return True
            except Exception as e:
                self.logger.error(f"Not enable to close the connection because '{e}' exception")
                raise e
        return False

    async def publish_msg(self, msg:str)->None:
        """
        Publishes (i.e.:sends) a message to the queue
        :param msg: message
        """
        await self.channel.default_exchange.publish( aio_pika.Message(
                                                                        body=msg.encode('utf-8')),
                                                                        routing_key=self.queue_name)

    async def consume_msg(self, process_message:Callable)->None:
        """
        consumes a message from the queue
        :param process_message: callable function (e.g.: PV_simulator.process_message)
        """
        await self.message_queue.consume(process_message, no_ack=True)