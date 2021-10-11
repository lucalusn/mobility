import unittest
import asyncio
from pv_simulator import Meter,Broker
from datetime import datetime
from json import loads

import logging

logging.basicConfig(filename="logger.log",
					format='%(asctime)s %(message)s',
					filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class invalid_Broker_param_test(unittest.TestCase):
    """
    Test case of not valid configuration file
    """
    broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)
    meter = Meter.Meter(min_power=0, max_power=1000, delta_time=2, broker=broker, logger=logger)

    def test_unable_to_connect(self):
        with self.assertRaises(Exception) as e:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.meter.open_connection())

        self.assertIsNone(self.meter.broker.channel)
        self.assertIsNone(self.meter.broker.connection)
        self.assertIsNone(self.meter.broker.message_queue)
        self.assertEqual(str(e.exception), "host and port was not specified and no sock specified")


class fake_connection_to_close_test(unittest.TestCase):
    """
    Test case of fake connection
    """
    def test_fake_connection_to_close(self):
        broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)
        meter = Meter.Meter(min_power=0, max_power=1000, delta_time=2, broker=broker, logger=logger)
        loop = asyncio.get_event_loop()
        meter.broker.connection = True
        with self.assertRaises(Exception) as e:
            loop.run_until_complete(meter.close_connection())
        self.assertEqual(str(e.exception), "'bool\' object has no attribute \'close'")


class valid_param_test(unittest.TestCase):
    """
    Test real case scenario
    """
    broker = Broker.Broker(address='amqp://guest:guest@localhost:5672/', queue_name='prova', logger=logger)
    meter = Meter.Meter(min_power=0, max_power=1000, delta_time=2, broker=broker, logger=logger)

    def test_enable_to_connect_and_close(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.meter.open_connection())
        self.assertFalse(self.meter.broker.connection.is_closed)
        self.assertFalse(self.meter.broker.channel.is_closed)
        self.assertEqual(self.meter.broker.channel.number,1)
        self.assertEqual(self.meter.broker.message_queue.name, 'prova')

        loop.run_until_complete(self.meter.close_connection())
        self.assertTrue(self.meter.broker.connection.is_closed)
        self.assertTrue(self.meter.broker.channel.is_closed)

    def test_send_message(self):
        def process_message():
            pass
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.meter.open_connection())

        # send message
        loop.run_until_complete(self.meter.send_messages(only_one=True))

        # read sent message
        published_message = loop.run_until_complete( self.meter.broker.message_queue.get(timeout=5))
        h_ts,min_ts,sec_ts = loads(published_message.body.decode('utf-8'))['Timestamp'].split(" ")[1].split("_")
        tot_sec_ts = int(sec_ts) + int(min_ts) * 60 + int(h_ts) * 24
        now=datetime.now().strftime("%m-%d-%Y %H_%M_%S")
        h_now,min_now,sec_now=now.split(" ")[1].split("_")

        # compare the time (in second) Do not run it at the turn of midnight ( :P)
        self.assertTrue(tot_sec_ts < int(sec_now) + int(min_now) * 60 + int(h_now) * 24 < tot_sec_ts+30)
        loop.run_until_complete(self.meter.broker.consume_msg(process_message))
        loop.run_until_complete(self.meter.close_connection())

if __name__ == '__main__':
    unittest.main()
