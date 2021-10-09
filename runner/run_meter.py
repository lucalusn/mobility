from pv_simulator import Broker, Meter, arg_parser
import asyncio

async def main_meter():
	args = arg_parser.create_parser().parse_args()
	cfg_rabbit = arg_parser.get_cfg_rabbitMQ(args.config_rabbitMQ)
	cfg_services = arg_parser.get_cfg_services(args.services_param)
	broker = Broker.Broker(address=cfg_rabbit['address'], queue_name=cfg_rabbit['queue_name'])
	meter = Meter.Meter(min_power=cfg_services['meter_min_power'], max_power=cfg_services['meter_max_power'], broker=broker, delta_time=cfg_services['delta_time'])

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