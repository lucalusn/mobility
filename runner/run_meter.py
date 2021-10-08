
from pv_simulator import Broker,Meter
import asyncio

async def main_meter():
	broker = Broker.Broker(address="amqp://guest:guest@localhost:5672/", queue_name="prova")
	meter = Meter.Meter(min_power=0, max_power=9000, broker=broker, delta_time=2)

	try:
		await meter.open_connection()  # Open connection with the Broker
		await meter.send_messages()    # Start sending data to queue
	finally:
		await meter.close_connection()

def run_meter():
	try:
		asyncio.run(main_meter())  # run forever
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	run_meter()