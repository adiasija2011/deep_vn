#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:34:10 2023

@author: adi10
"""


#arrival probability of packet: bernoulli
#service probability of packet:geometric

# p = 1 q = 1 to receive packets the next time step
p = 1  
q = 1

#mode to save files
mode = '0.2q'

#number of cars in environment
t_car = 1

#penalising parameters
#state penalty
Q = 10.0

#control penalty
R = 5.0

#weight factor
#0.005,0.05,0.1,0.2,0.6,0.8,1
lamda = 0.2