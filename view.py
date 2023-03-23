#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:36:18 2023

@author: adi10
"""

from collections import defaultdict
from math import pi,sin,cos


class ego_view():
    def __init__(self,veh_id,env):
        self.local_view = defaultdict()
        self.extended_view = defaultdict()
        self.veh_id = veh_id
        self.env = env
        self.extended_view_radius = 100
        self.local_view_radius = 50
        
    def get_cars(self):
        all_veh_id = self.env.k.vehicle.get_ids()
        ego_x , ego_y = self.env.k.kernel_api.vehicle.getPosition("rl_0")[0] , \
            self.env.k.kernel_api.vehicle.getPosition("rl_0")[1]

        for car in all_veh_id:
            car_x, car_y = self.env.k.kernel_api.vehicle.getPosition(car)[0], \
                self.env.k.kernel_api.vehicle.getPosition(car)[1]

            """
            update local view with age 0 and all current measurements
            """
            if (ego_x - self.local_view_radius) < car_x < (ego_x + self.local_view_radius) and \
                    (ego_y - self.local_view_radius) < car_y < (ego_y + self.local_view_radius):
                theta = self.env.k.kernel_api.vehicle.getAngle(car) * (pi / 180)
                car_vel_x = self.env.k.kernel_api.vehicle.getSpeed(car)*cos(theta)
                car_vel_y = self.env.k.kernel_api.vehicle.getSpeed(car)*sin(theta)
                self.local_view[car] = [car_x , car_y , car_vel_x , car_vel_y , 0]

            """
            update extended view with age 0 and all current measurements 
            """

            if (ego_x - self.extended_view_radius) < car_x < (ego_x - self.local_view_radius) and \
                    (ego_y - self.extended_view_radius) < car_y < (ego_y - self.local_view_radius):
                theta = self.env.k.kernel_api.vehicle.getAngle(car) * (pi / 180)
                car_vel_x = self.env.k.kernel_api.vehicle.getSpeed(car)*cos(theta)
                car_vel_y = self.env.k.kernel_api.vehicle.getSpeed(car)*sin(theta)
                self.extended_view[car] = [car_x , car_y , car_vel_x , car_vel_y , 0]

        return None
    
        
        
        
        
