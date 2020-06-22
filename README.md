# Notes for Simulation

Author: Shan Yang, Wang Zilu

From: Department of Mangement Science and Engineering, Tongji University

E-mail: tjyangshan@gmail.com, prinway1226@gmail.com

## Introduction

This repository mainly contains our notes about some examples of SimPy. It also contains teaching examples using Excel from Prof. Qiu Canhua and Prof. Hu Zhaolin. 

SimPy Documentation: https://simpy.readthedocs.io/en/latest/examples/index.html

We also build a demo for airplane boarding based on SimPy. https://github.com/seanys/Boarding-Simulation

## Examples-SimPy

### Bank Renege 

> A counter with a random service time and customers who renege. Based on the program bank08.py from TheBank tutorial of SimPy 2. (KGM)

Source Code&Notes(Chinese): [bank-renage.py](simpy-examples/bank-renage.py)

### Movie Renege

> A movie theatre has one ticket counter selling tickets for three movies (next show only). When a movie is sold out, all people waiting to buy tickets for that movie renege (leave queue).

Source Code&Notes(Chinese): [movie-renage.py](simpy-examples/movie-renage.py)

### Machine Shop

> A workshop has *n* identical machines. A stream of jobs (enough to keep the machines busy) arrives. Each machine breaks down periodically. Repairs are carried out by one repairman. The repairman has other, less important tasks to perform, too. Broken machines preempt theses tasks. The repairman continues them when he is done with the machine repair. The workshop works continuously.

Source Code&Notes(Chinese): [machine-shop.py](simpy-examples/machine-shop.py)

### Carwash

> A carwash has a limited number of washing machines and defines a washing processes that takes some (random) time. Car processes arrive at the carwash at a random time. If one washing machine is available, they start the washing process and wait for it to finish. If not, they wait until they an use one.

Source Code&Notes(Chinese): [carwash.py](simpy-examples/carwash.py)

### Event Latency

> This example shows how to separate the time delay of events between processes from the processes themselves.

Source Code&Notes(Chinese): [event-latency.py](simpy-examples/event-latency.py)

### Gas Station Refueling Example

> A gas station has a limited number of gas pumps that share a common fuel reservoir. Cars randomly arrive at the gas station, request one of the fuel pumps and start refueling from that reservoir. A gas station control process observes the gas station's fuel level and calls a tank truck for refueling if the station's level drops below a threshold.

Source Code&Notes(Chinese): [gas-station-refueling.py](simpy-examples/gas-station-refueling.py)

It is also a simple exmaple for inventory management.

### Process Communication

> This example shows how to interconnect simulation model elements together using :class : `~simpy.resources.store.Store` for one-to-one, and many-to-one asynchronous processes. For one-to-many a simpleBroadCastPipe class is constructed from Store.

Source Code&Notes(Chinese): [process-communication.py](simpy-examples/process-communication.py)

### Example-Excel

https://github.com/seanys/Operations-Management#simulation

https://github.com/seanys/Simulation-Notes/tree/master/excel-examples



