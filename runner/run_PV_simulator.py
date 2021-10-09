from pv_simulator import Broker,Meter,PV_simulator,arg_parser
import asyncio

async def main_pv():
	args = arg_parser.create_parser().parse_args()
	cfg_rabbit = arg_parser.get_cfg_rabbitMQ(args.config_rabbitMQ)
	cfg_services = arg_parser.get_cfg_services(args.services_param)
	broker = Broker.Broker(address=cfg_rabbit['address'], queue_name=cfg_rabbit['queue_name'])

	simulator = PV_simulator.PV_simulator(address=cfg_rabbit['address'],
										  queue_name=cfg_rabbit['queue_name'],
										  broker=broker,
										  max_pv=cfg_services['pv_max_power'] / 1000,
										  delta_time=cfg_services['delta_time'],
										  out_folder=cfg_services['output_folder'])
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