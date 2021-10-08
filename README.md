###### General:
System that collects every 'n' seconds data from a Meter, which generates random values between 0-9kW for mocking a regular home power consumption, generates simulated PV (photovoltaic) power values (in kW) and write these results on file.

The following picture of a real PV power output curve during a normal day.

![Image of real data](real curve.png)
 
The following picture represent the simulated PV power output curve

![Image of simulated data](simulated data_PV.png)


###### Architecture:

* **Meter** produces messages to the broker with random but continuous values from 0 to 9000 Watts.This is to mock a regular home power consumption.

* **Broker** is a RabbitMQ is a message-queueing software. More info about [rabbitMQ](https://www.rabbitmq.com/)

* **PV simulator** listens to the broker for the meter values, generate a simulated PV power value and adds this value to the meter value and output the result.

* **Output** is the save on file step. The result are collected every couple of seconds in the following format (timestamp, meter power value, PVpower valueand the sum of the powers (meter + PV)).

The following diagram exemplifies the interactions between the components

![Image of system architecture](architecture.png)

###### How to install:
1: create a conda env and install the package using setup.py

    conda create -n mobility python=3
    source activate mobility

2: clone repository

    git clone https://github.com/lucalusn/mobility.git

3: build package xy

    cd mobility
    python setup.py sdist
    pip install dist/mobility-X.Y.Z.tar.gz    

###### Example of use:

Just run the main

    pv_main 
    
###### Parameters meaning
    -p1: 
    -p2:

