import unittest
from pv_simulator import PV_simulator, Broker, Meter
from datetime import datetime
import asyncio
from os import remove,path

import logging

logging.basicConfig(filename="logger.log",
					format='%(asctime)s %(message)s',
					filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class gauss_test(unittest.TestCase):
    def test_gauss(self):
        self.assertAlmostEqual(1.5966859,PV_simulator.gauss(x=10,A=3.4,mu=13,sigma=2.44),5)


class get_sec_test(unittest.TestCase):
    def test_get_sec(self):
        self.assertEqual(53759,PV_simulator.get_sec(datetime(year=2020, month=11, day=28, hour=14, minute=55, second=59).strftime("%m-%d-%Y %H_%M_%S")))
        self.assertEqual(0,PV_simulator.get_sec(datetime(year=2020, month=11, day=28, hour=0, minute=0, second=0).strftime("%m-%d-%Y %H_%M_%S")))


class invalid_Broker_param_test(unittest.TestCase):
    """
    Test case of not valid configuration file
    """
    broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)
    simulator = PV_simulator.PV_simulator(broker=broker,
                                          max_pv=3.4,
                                          delta_time=2,
                                          out_folder=".",
                                          logger=logger)

    def test_unable_to_connect(self):
        with self.assertRaises(Exception) as e:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.simulator.connect_to_broker())

        self.assertIsNone(self.simulator.broker.channel)
        self.assertIsNone(self.simulator.broker.connection)
        self.assertIsNone(self.simulator.broker.message_queue)
        self.assertEqual(str(e.exception), "host and port was not specified and no sock specified")


class fake_connection_to_close_test(unittest.TestCase):
    """
    Test case of fake connection
    """
    def test_fake_connection_to_close(self):
        broker = Broker.Broker(address='invalid_add', queue_name='queue_name', logger=logger)
        simulator = PV_simulator.PV_simulator(broker=broker,
                                              max_pv=3.4,
                                              delta_time=2,
                                              out_folder=".",
                                              logger=logger)
        loop = asyncio.get_event_loop()
        simulator.broker.connection = True
        with self.assertRaises(Exception) as e:
            loop.run_until_complete(simulator.disconnect_to_broker())
        self.assertEqual(str(e.exception), "'bool\' object has no attribute \'close'")



class valid_param_test(unittest.TestCase):
    """
    Test real case scenario
    """
    broker = Broker.Broker(address='amqp://guest:guest@localhost:5672/', queue_name='prova', logger=logger)
    meter = Meter.Meter(min_power=0, max_power=1000, delta_time=2, broker=broker, logger=logger)
    simulator = PV_simulator.PV_simulator(broker=broker,
                                          max_pv=3.4,
                                          delta_time=2,
                                          out_folder=".",
                                          logger=logger)

    def test_enable_to_connect_and_close(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.simulator.connect_to_broker())
        self.assertFalse(self.simulator.broker.connection.is_closed)
        self.assertFalse(self.simulator.broker.channel.is_closed)
        self.assertEqual(self.simulator.broker.channel.number,1)
        self.assertEqual(self.simulator.broker.message_queue.name, 'prova')

        loop.run_until_complete(self.simulator.disconnect_to_broker())
        self.assertTrue(self.simulator.broker.connection.is_closed)
        self.assertTrue(self.simulator.broker.channel.is_closed)

    def test_write_on_file(self):
        data = {'Timestamp': str(datetime.now()),
                'Meter_value': 3333,
                'PV_value': 1.3,
                'Tot_value':3334}
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.simulator.write_on_file(data=data))
        loop.run_until_complete(self.simulator.write_on_file(data=data))
        remove(self.simulator.filename)

    def test_consume_data(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.meter.open_connection())
        loop.run_until_complete(self.simulator.connect_to_broker())

        # send message by meter
        loop.run_until_complete(self.meter.send_messages(only_one=True))

        # consume message
        loop.run_until_complete(self.simulator.consume_data())

        # check if the file has been created
        self.assertTrue(path.isfile(self.simulator.filename))

        if path.isfile(self.simulator.filename):
            f = open(self.simulator.filename, "r")
            lines = f.readlines()
            self.assertTrue("Timestamp" in lines[0])
            self.assertTrue("Meter_value" in lines[1])
            self.assertTrue("PV_value" in lines[2])
            self.assertTrue("Tot_value" in lines[3])
            today=str(datetime.now().strftime("%m-%d-%Y %H_%M_%S")).split(" ")[0]
            date_saved_msg = lines[5].split('\t')[0].split(" ")[0]
            self.assertEqual(today,date_saved_msg)   # if True it wrote the message
            f.close()
            remove(self.simulator.filename)

if __name__ == '__main__':
    unittest.main()
