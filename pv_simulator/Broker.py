"""
Is a message-queueing, a rabbitMQ, that allows 'Meter' and 'PV_simulator' to communicate with each other.
It receives messages from 'Meter' and sends them to 'PV_simulator'
"""
import pika

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

    def connect(self)->None:
        """
        Create the connection and declare the queue
        In case it is not possible to create the connection an error message will explain the reason
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.address))
            self.channel = self.connection.channel()
            self.channel.queue_declare(self.queue_name)
        except Exception as e:
            print (f"Not enable to create the connection because '{e}' exception")
            raise e

    def close(self)->None:
        """
        Closes the connection between Meter and PV_simulator
        In case it is not possible to close the connection an error message will explain the reason
        """
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Not enable to close the connection because '{e}' exception")
                raise e

    def send_msg(self, msg:str)->None:
        """
        Sends the message to the queue
        :param msg: message
        """
        pass

    def receive_msg(self)->None:
        """
        receives the message to the queue
        """
        pass