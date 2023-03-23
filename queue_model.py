#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:29:09 2023

@author: adi10
"""



import numpy as np
import queue_config as config
import pdb
import random
from copy import deepcopy

"""
This implementation is same as queue_model.py but done in the form of a class in order to instantiate multiple objects.
To instantiate an object of this class (p,q) values to need to be given in the initialization call.  
"""
class queue_model:
    def __init__(self,p,q):
        self.q=q
        self.p=p
        self.packet_service = False
        self.time_remain = -1
        self.buffer = 0
        self.pkt_0 = {}
        self.queue=[]

    def queueing(self, packet, reset=False):

        if reset == True:
            self.packet_service = False
            self.time_remain = -1
            self.buffer= 0
            self.pkt_0 = {}

        # q = config.q
        q=self.q
        # Buffer.
        #   pdb.set_trace()
        # packet_arrived = self.arrival(config.p)
        packet_arrived = self.arrival()
        if packet_arrived == 1:

            # if packet arrives, append for ego vehicle also
            # queue[first_element][time_stamp][packet_of_car]
            self.queue.append(deepcopy(packet))
            self.buffer += 1

            # if any packet is not in service
            if self.packet_service != True:
                # reduce buffer size and send last packet from queue for service
                self.buffer = self.buffer - 1
                slots = np.random.geometric(q)

                #         pdb.set_trace()

                self.pkt_0 = self.queue.pop(0)

                #         print('Packet in transit',pkt_0)
                self.time_remain = self.transmission(slots)
                return self.queue, {}

        # if any packet is already in service
            else:
                # move to next time  step but check for completion of transmission
                #         pdb.set_trace()
                if self.time_remain >= 0:
                    self.time_remain = self.time_remain - 1
                self.packet_service = self.check_transmission(self.time_remain)

            # if packet service has ended, return the packets to be delivered at car,
            # catched by transit_pkt and start another transmission

            if self.packet_service == False:


                self.buffer = self.buffer - 1
                slots = np.random.geometric(q)

                # make a deep copy of packet to car
                pkt_1 = deepcopy(self.pkt_0)
                # pop the element and send for transmission
                self.pkt_0 = self.queue.pop(0)
                self.time_remain = self.transmission(slots)
                #            print('Packet in transit',pkt_0)

                return self.queue, pkt_1
            else:
                return self.queue, {}

            # no packet arrived
        else:
            if self.packet_service != True:


                # check if buffer is empty, if empty
                if not self.buffer:
                    return self.queue, {}

                # buffer is not empty
                else:
                    slots = np.random.geometric(q)
                    self.pkt_0 = self.queue.pop(0)
                    self.buffer = self.buffer - 1
                    self.time_remain = self.transmission(slots)

                    return self.queue, {}
            # packet is in transit, just check for transmission
            else:
                if self.time_remain >= 0:
                    self.time_remain = self.time_remain - 1
                self.packet_service = self.check_transmission(self.time_remain)

                # if packet service has ended, then return packets to be sent to car,send packet
                # for transmission to send if buffer not empty
                if self.packet_service == False:
                    if self.queue:
                        self.buffer = self.buffer - 1
                        slots = np.random.geometric(q)
                        pkt_1 = deepcopy(self.pkt_0)
                        self.pkt_0 = self.queue.pop(0)
                        #              pdb.set_trace()
                        #               print('Packet in transit',pkt_0)
                        self.time_remain = self.transmission(slots)
                        return self.queue, pkt_1
                    else:
                        return self.queue, self.pkt_0
                else:
                    return self.queue, {}

            # %%transmission to the car
    def transmission(self,time_service):
        """
        Parameters
        ----------
        time_service : time slots for successfull transmission of packet to the car

        Returns
        -------
        time_service : remaining slot

        """
        # global time_remain
        # global packet_service
        self.packet_service = True
        self.time_remain = time_service - 1
        return self.time_remain

            # %%check completed transmission
    def check_transmission(self,time_remain):
        """
               Parameters
                ----------
                time_remain : time slots remaining

                Returns
                -------
                packet_service
                """
        # global packet_service

        if time_remain == -1:
            self.packet_service = False
        else:
            self.packet_service = True
        return self.packet_service

            # %%packet arrival at the channel
    def arrival(self):
        """
                Parameters
                ----------
                p : packet arrival rate

                Returns
                -------
                packet_arrive : whether packet has been arrived or not

                """

        p = self.p
        # corrected with binomial distribution
        packet_arrive = np.random.binomial(1, p)
        # packet_arrive = bernoulli.rvs(p)
        return packet_arrive

            # %%generate random velocity and position
    def generate(v=0):
        """
            Parameters
            ----------
            v : car_id

            Returns
            -------
            Position and velocity

            """

        if v == None:
            # car id, random number between 1-10
            v = random.randint(1, 9)
            # position between 0-5 f0r x and 0 for y for now
            px = random.randint(0, 5)
            # velocity between 0-1 for x and 0 for y
            vx = round(random.uniform(0, 1), 2)
            return v, px, vx


