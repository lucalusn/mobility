import unittest
import asyncio
from pv_simulator import Broker
from aio_pika import IncomingMessage
from datetime import datetime
from json import dumps,loads

import logging

logging.basicConfig(filename="logger.log",
					format='%(asctime)s %(message)s',
					filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class invalid_param_test(unittest.TestCase):
    broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)

    def test_unable_to_connect(self):
        with self.assertRaises(Exception) as e:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.broker.connect())

        self.assertIsNone(self.broker.channel)
        self.assertIsNone(self.broker.connection)
        self.assertIsNone(self.broker.message_queue)
        self.assertEqual(str(e.exception), "host and port was not specified and no sock specified")

    def test_no_connection_to_close(self):
        loop = asyncio.get_event_loop()
        self.assertFalse(loop.run_until_complete(self.broker.close()))

class fake_connection_to_close_test(unittest.TestCase):
    def test_fake_connection_to_close(self):
        broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)
        loop = asyncio.get_event_loop()
        broker.connection = True
        with self.assertRaises(Exception) as e:
            loop.run_until_complete(broker.close())
        a=str(e.exception)
        self.assertEqual(str(e.exception), "'bool\' object has no attribute \'close'")



class valid_param_test(unittest.TestCase):
    broker = Broker.Broker(address='amqp://guest:guest@localhost:5672/', queue_name='prova', logger=logger)

    def test_enable_to_connect_and_close(self):
        loop = asyncio.get_event_loop()
        self.assertTrue(loop.run_until_complete(self.broker.connect()))
        self.assertFalse(self.broker.connection.is_closed)
        self.assertFalse(self.broker.channel.is_closed)
        self.assertEqual(self.broker.channel.number,1)
        self.assertEqual(self.broker.message_queue.name, 'prova')

        self.assertTrue(loop.run_until_complete(self.broker.close()))
        self.assertTrue(self.broker.connection.is_closed)
        self.assertTrue(self.broker.channel.is_closed)

    def test_publish_message(self):

        loop = asyncio.get_event_loop()
        self.assertTrue(loop.run_until_complete(self.broker.connect()))

        msg  = {'Timestamp':str(datetime.now().strftime("%m-%d-%Y %H_%M_%S")),'Meter_value': 1}
        loop.run_until_complete(self.broker.publish_msg(msg=dumps(msg)))
        published_message = loop.run_until_complete( self.broker.message_queue.get(timeout=5))
        body=loads(published_message.body.decode('utf-8'))
        self.assertEqual(msg['Meter_value'],body['Meter_value'])
        self.assertTrue(loop.run_until_complete(self.broker.close()))

    def test_consume_message(self):
        def process_message(pub_msg: IncomingMessage)->str:
            """
            Callback function for receiving the message from the message queue
            :param pub_msg: message got from the queue
            :return: the body of the message as string
            """
            self.assertTrue(msg,str(pub_msg.body, 'UTF-8'))
            return str(pub_msg.body, 'UTF-8')

        loop = asyncio.get_event_loop()
        self.assertTrue(loop.run_until_complete(self.broker.connect()))

        msg  = {'Timestamp':str(datetime.now().strftime("%m-%d-%Y %H_%M_%S")),'Meter_value': 1}
        loop.run_until_complete(self.broker.publish_msg(msg=dumps(msg)))

        loop.run_until_complete(self.broker.consume_msg(process_message))

        self.assertTrue(loop.run_until_complete(self.broker.close()))

if __name__ == '__main__':
    unittest.main()
