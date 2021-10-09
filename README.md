## General:
System that collects every 'n' seconds data from a Meter, which generates random values between 0-9kW for mocking a regular home power consumption, generates simulated PV (photovoltaic) power values (in kW) and write these results on file.

The following picture of a real PV power output curve during a normal day.

![Image of real_data](https://github.com/lucalusn/mobility/blob/main/images/real_curve.png)
 
The following picture represent the simulated PV power output curve

![Image of simulated_data](https://github.com/lucalusn/mobility/blob/main/images/simulated_data_PV.png)


## Architecture:

* **Meter** produces messages to the broker with random but continuous values from 0 to 9000 Watts.This is to mock a regular home power consumption.

* **Broker** is a RabbitMQ is a message-queueing software. More info about [rabbitMQ](https://www.rabbitmq.com/)

* **PV simulator** listens to the broker for the meter values, generate a simulated PV power value and adds this value to the meter value and output the result.

* **Output** is the save on file step. The result are collected every couple of seconds in the following format (timestamp, meter power value, PVpower valueand the sum of the powers (meter + PV)). 
The filename will be generated automatically from the script in function of the execution time in the folder specified by the user. If the folder does not exist the result will be saved in the HOME directory. Name format: logfile_month_day_year_hour_min_sec.log

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

2. run  the script **pv_main.py -c demo_cfg_rabbitMQ.json -v demo_cfg_services.json** 

3. Run the **docker-compose down** command in a terminal for closing the rabbitMQ
    
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
