"""
Is a message-queueing, a rabbitMQ, that allows 'Meter' and 'PV_simulator' to communicate with each other.
It receives messages from 'Meter' and sends them to 'PV_simulator'
"""
import aio_pika
from typing import Callable

class Broker:
    def __init__(self,address: str, queue_name:str)->None:
        """
        :param address: address of a broker (e.g: 'localhost' or IP address)
        :param queue_name: Name of the rabbitMQ queue
        """
        self.address = address
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.message_queue = None

    async def connect(self)->None:
        """
        Create the connection and declare the queue
        In case it is not possible to create the connection an error message will explain the reason
        """
        try:
            self.connection = await aio_pika.connect(self.address)
            self.channel = await self.connection.channel()
            self.message_queue = await self.channel.declare_queue(self.queue_name)
        except Exception as e:
            print (f"Not enable to create the connection because '{e}' exception")
            raise e

    async def close(self)->None:
        """
        Closes the connection between Meter and PV_simulator
        In case it is not possible to close the connection an error message will explain the reason
        """
        if self.connection:
            try:
                await self.connection.close()
            except Exception as e:
                print(f"Not enable to close the connection because '{e}' exception")
                raise e

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