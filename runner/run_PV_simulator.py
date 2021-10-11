from pv_simulator import Broker,PV_simulator,arg_parser
import asyncio
from pathlib import Path
from os import path
import logging
from datetime import datetime

async def main_pv():
	args = arg_parser.create_parser().parse_args()
	cfg_rabbit = arg_parser.get_cfg_rabbitMQ(args.config_rabbitMQ)
	cfg_services = arg_parser.get_cfg_services(args.services_param)

	logger_folder= cfg_services['output_folder'] if cfg_services['output_folder'] is not None and path.isdir(cfg_services['output_folder']) else str(Path.home())
	logging.basicConfig(filename=path.join(logger_folder,'logger_pv_simulator_'+datetime.now().strftime("%m_%d_%Y %H_%M_%S").replace(" ","_")+".log"),
						format='%(asctime)s %(message)s',
						filemode='w')
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