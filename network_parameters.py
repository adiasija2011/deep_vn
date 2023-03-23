#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:51:48 2023

@author: adi10
"""


ADDITIONAL_ENV_PARAMS = {
    
    # maximum acceleration for autonomous vehicles, in m/s^2
    "max_accel": 3,
    
    # maximum deceleration for autonomous vehicles, in m/s^2
    "max_decel": 3,
    
    # lane change duration for autonomous vehicles, in s. Autonomous vehicles
    # reject new lane changing commands for this duration after successfully
    # changing lanes.
    "lane_change_duration": 0.1,
    
    # desired velocity for all vehicles in the network, in m/s
    "target_velocity": 10,
    
    # specifies whether vehicles are to be sorted by position during a
    # simulation step. If set to True, the environment parameter
    # self.sorted_ids will return a list of all vehicles sorted in accordance
    # with the environment
    'sort_vehicles': False,
   
}


USER_NETWORK_PARAMS ={
    
    #horizon for experiment 
    "horizon" : 10000,
    
    #simulation step in seconds
    "sim_step" : 0.1,
    
    #render gui
    "render" : True,
    
    #number of highway lanes
    "highway_lanes" : 4,
    
    #number of merge lanes
    "merge_lanes":2
    }

