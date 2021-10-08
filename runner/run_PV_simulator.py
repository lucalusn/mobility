from pv_simulator import Broker,Meter,PV_simulator
import asyncio

async def main_pv():
	add = "amqp://guest:guest@localhost:5672/"
	qname="prova"
	broker = Broker.Broker(address=add, queue_name=qname)
	simulator = PV_simulator.PV_simulator( address= add,
                 queue_name = qname,
                 broker = broker,
                 max_pv = 2.4,
                 delta_time= 2)
	try:
		await simulator.connect_to_broker()  # Enable the connection between Simulator & Broker
		await simulator.consume_data()  # Start consuming data from queue
	finally:
		await simulator.disconnect_to_broker()


def run_PV():
	try:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(main_pv())
		loop.run_forever()
	except KeyboardInterrupt:
		pass


if __name__ == "__main__":
	run_PV()