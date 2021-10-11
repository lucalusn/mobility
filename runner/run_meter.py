from pv_simulator import Broker, Meter, arg_parser
import asyncio
from pathlib import Path
from os import path
import logging
from datetime import datetime


async def main_meter():
	args = arg_parser.create_parser().parse_args()
	cfg_rabbit = arg_parser.get_cfg_rabbitMQ(args.config_rabbitMQ)
	cfg_services = arg_parser.get_cfg_services(args.services_param)

	logger_folder = cfg_services['output_folder'] if cfg_services['output_folder'] is not None and path.isdir(cfg_services['output_folder']) else str(Path.home())
	logging.basicConfig(filename=path.join(logger_folder, 'logger_meter._'+datetime.now().strftime("%m_%d_%Y %H_%M_%S").replace(" ","_")+".log"),
						format='%(asctime)s %(message)s',
						filemode='w')
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	broker = Broker.Broker(address=cfg_rabbit['address'], queue_name=cfg_rabbit['queue_name'],logger=logger)
	meter = Meter.Meter(min_power=cfg_services['meter_min_power'], max_power=cfg_services['meter_max_power'],
						broker=broker, delta_time=cfg_services['delta_time'], logger=logger)

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