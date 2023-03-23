#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:33:22 2023

@author: adi10
"""
import numpy as np
# import pdb

from merge_network import simulator
from view import ego_view


#import IDM controller to control ego vehicle
from flow.controllers import IDMController
from flow.core.params import SumoCarFollowingParams

merge_sim = simulator()
merge_env = merge_sim.create_gym_env()

NUM_STEPS = 1000
NUM_EPISODES = 1
done = False


cntrl_idm = IDMController(veh_id = "rl_0",
                          car_following_params =SumoCarFollowingParams(
                              speed_mode="obey_safe_speed"))

rl_view = ego_view( "rl_0", merge_env)

for i in range(NUM_EPISODES):
    merge_env.reset()
    for j in range(NUM_STEPS):
        if done == False:
            #action = [idm_acceleration,no lane change]
            trial = rl_view.get_cars()
            actions = np.array([cntrl_idm.get_accel(env = merge_env) , 0])
            state, reward , done , info =  merge_env.step(actions)
        else:
            break
        
    
    