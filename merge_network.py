#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:50:29 2023

@author: adi10
"""


#import all libraries 
from flow.core.experiment import Experiment
from flow.core.params import NetParams, EnvParams, InitialConfig, InFlows,\
    VehicleParams, SumoParams, SumoCarFollowingParams,\
        RLController, SumoLaneChangeParams
                                 
from flow.controllers import IDMController
from flow.networks import MergeNetwork
from flow.networks.merge import ADDITIONAL_NET_PARAMS
from flow.envs.ring.lane_change_accel import LaneChangeAccelEnv
from flow.utils.registry import make_create_env


from network_parameters import ADDITIONAL_ENV_PARAMS, USER_NETWORK_PARAMS




class simulator():
    
    def __init__(self):

        # create a vehicle type
        self.vehicles = VehicleParams()
    
        #create human driven vehicles which change lanes and follow IDM
        self.vehicles.add("human",
                          acceleration_controller=(IDMController, {}),
                          car_following_params=SumoCarFollowingParams(
                              speed_mode="obey_safe_speed"),
                          lane_change_params=\
                              SumoLaneChangeParams(lane_change_mode=1621))
    
        #create ego vehicle 
        self.vehicles.add("rl",
                          acceleration_controller=(RLController, {}),
                          car_following_params=SumoCarFollowingParams(),
                          color='yellow',
                          num_vehicles=1,
                          initial_speed=0.0)

        # create the inflows
        self.inflows = InFlows()
        # inflow for (1)
        self.inflows.add(veh_type="human",
                         edge="inflow_highway",
                         vehs_per_hour=10000,
                         depart_lane="random",
                         depart_speed="random",
                         color="white")

        # inflow for (2)
        self.inflows.add(veh_type="human",
                         edge="inflow_merge",
                         period=2,
                         depart_lane=0,  # right lane
                         depart_speed=0,
                         color="green")

        # inflow for (3)
        self.inflows.add(veh_type="human",
                         edge="inflow_merge",
                         probability=0.1,
                         depart_lane=1,  # left lane
                         depart_speed="max",
                         begin=60,  # 1 minute
                         number=30,
                         color="red")






        # modify the network accordingly to instructions
        # (the available parameters can be found in flow/networks/merge.py)
        additional_net_params = ADDITIONAL_NET_PARAMS.copy()
        
        # this is just for visuals
        additional_net_params['post_merge_length']=350  
        
        additional_net_params['highway_lanes'] \
            =USER_NETWORK_PARAMS["highway_lanes"]
        additional_net_params['merge_lanes'] \
            =USER_NETWORK_PARAMS["merge_lanes"]
    
        # setup and run the simulation
        self.net_params = NetParams(inflows=self.inflows,
                                    additional_params=additional_net_params)
    
        self.sim_params = SumoParams(render=USER_NETWORK_PARAMS["render"],
                                sim_step=USER_NETWORK_PARAMS["sim_step"])
    
        self.sim_params.color_vehicles = False
    
        self.env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)
    
        self.initial_config = InitialConfig()
    
        self.flow_params = dict(
            exp_tag='merge-example',
            env_name=LaneChangeAccelEnv,
            network=MergeNetwork,
            simulator='traci',
            sim=self.sim_params,
            env=self.env_params,
            net=self.net_params,
            veh=self.vehicles,
            initial=self.initial_config,
            )
    
        # number of time steps
        self.flow_params['env'].horizon = USER_NETWORK_PARAMS["horizon"]
        self.exp = Experiment(self.flow_params)
    
    def create_gym_env(self):
        # run the sumo simulation
        create_env, gym_name = make_create_env(
            params=self.flow_params, version=0)
        
        merge_env = create_env()
        
        return merge_env

    
    
