from pv_simulator import Broker,Meter,PV_simulator,arg_parser
import asyncio

# importing module
import logging

logging.basicConfig(filename="logger_pv_simulator.log",
					format='%(asctime)s %(message)s',
					filemode='w')
async def main_pv():
	args = arg_parser.create_parser().parse_args()
	cfg_rabbit = arg_parser.get_cfg_rabbitMQ(args.config_rabbitMQ)
	cfg_services = arg_parser.get_cfg_services(args.services_param)

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	broker = Broker.Broker(address=cfg_rabbit['address'], queue_name=cfg_rabbit['queue_name'],logger=logger)

	simulator = PV_simulator.PV_simulator(broker=broker,
										  max_pv=cfg_services['pv_max_power'] / 1000,
										  delta_time=cfg_services['delta_time'],
										  out_folder=cfg_services['output_folder'],
										  logger=logger)
	try:
		await simulator.connect_to_broker()  # Enable the connection between Simulator & Broker
		await simulator.consume_data()  # Start consuming data from queue
	except :
		pass


def run_PV():
	try:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(main_pv())
		loop.run_forever()
	except KeyboardInterrupt:
		pass


if __name__ == "__main__":
	run_PV()