[![Build Status](https://app.travis-ci.com/lucalusn/mobility.svg?branch=main)](https://app.travis-ci.com/github/lucalusn/mobility)
[![codecov](https://codecov.io/gh/lucalusn/mobility/branch/main/graph/badge.svg?token=IC77RKXPWO)](https://codecov.io/gh/lucalusn/mobility)

## General:
System that collects every 'n' seconds data from a Meter, which generates random values between 0-9kW for mocking a regular home power consumption, generates simulated PV (photovoltaic) power values (in kW) and write these results on file.

The following picture represents the real PV power output curve during a normal day.

![Image of real_data](https://github.com/lucalusn/mobility/blob/main/images/real_curve.png)
 
The following picture represents the simulated PV power output curve

![Image of simulated_data](https://github.com/lucalusn/mobility/blob/main/images/simulated_data_PV.png)


## Architecture:

* **Meter** produces messages to the broker with random but continuous values from 0 to 9000 Watts.This is to mock a regular home power consumption.

* **Broker** is a RabbitMQ is a message-queueing software. More info about [rabbitMQ](https://www.rabbitmq.com/)

* **PV simulator** listens to the broker for the meter values, generate a simulated PV power value and adds this value to the meter value and output the result.

* **Output** is the save on file step. The result are collected every couple of seconds in the following format (timestamp, meter power value, PV power value and the sum of the powers (meter + PV)). 
The filename will be generated automatically from the script in function of the starting time in the folder specified by the user. If the folder does not exist the result will be saved in the $HOME directory. Name format: result_<month>_<day>_<year>_<hour>_<min>_<sec>.txt

The following diagram exemplifies the interactions between the components

![Image of system architecture](https://github.com/lucalusn/mobility/blob/main/images/architecture.png)

## How to install:
This demo script will run the RabbitMQon on a docker container. **Docker** and **Docker-compose** have to be manually install on your machine. 
More info about how to install [Docker](https://docs.docker.com/engine/install/ubuntu/) and [Docker-compose](https://docs.docker.com/compose/install/)

1: create a conda env and install the package using setup.py

    conda create -n mobility python=3
    source activate mobility

2: clone repository

    git clone https://github.com/lucalusn/mobility.git

3: build package xy

    cd mobility
    python setup.py sdist
    pip install dist/mobility-X.Y.Z.tar.gz    

## Example of use:

1. Run the **docker-compose up -d** command in a terminal for starting the rabbitMQ, wait for the command to complete its execution. You have to be in the same directory of a **docker-compose.yaml** file.

2. run in in separate terminals the following scripts (NB: the scripts are in the **/<path_to_your_conda/envs/mobility/bin/** folder)
    - **run_meter.py -c <path_to_the_repo>/runner/demo_cfg_rabbitMQ.json -v <path_to_the_repo>/runner/demo_cfg_services.json** 
    - **run_PV_Simulator.py -c <path_to_the_repo>/runner/demo_cfg_rabbitMQ.json -v <path_to_the_repo>/runner/demo_cfg_services.json**

3. Run the **docker-compose down** command in a terminal for closing the rabbitMQ

## Tests coverage
For running the tests and show the result to the terminal:
python -m pytest -v <path_to_the_repo>/tests --cov-report term --cov= <path_to_the_repo>/pv_simulator

Actual coverage:

        Name                           Stmts   Miss  Cover
    --------------------------------------------------
    pv_simulator/Broker.py            28     20    29%
    pv_simulator/Meter.py             23     13    43%
    pv_simulator/PV_simulator.py      44     22    50%
    pv_simulator/__init__.py           1      0   100%
    pv_simulator/arg_parser.py        34     34     0%
    --------------------------------------------------
    TOTAL                            130     89    32%



## Parameters meaning
    -c: path to the json file containing the rabbitMQ access parameters. It is mandatory. List of fields
        * 'address' is the address of the rabbitMQ service
        * 'queue_name' is the name of the queue
    -v: path to the json file containing the services (Meter and PV simulator) access parameters. List of fields:
        * 'pv_max_power' is the estimated maximum photovoltaic value expressed in watt. Default value is 3400[W]
        * 'meter_max_power' is the estimated maximum home power consumption  value expressed in watt. Default value is 90000[W]
        * 'meter_min_power' is the estimated minimum home power consumption value expressed in watt. Default value is 0[W]
        * 'output_folder' is the path to the folder where the output file will be saved. Default value is ''
        * 'frequency' is the time between the creation/consumption of two consecutive messages
