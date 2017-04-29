#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 Martin Kauss (yo@bishoph.org)

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

# Robot arm

import os
import sys
import time
import usb.core, usb.util

RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x000)
light = 0

if (RoboArm != None):
    print ('Robotic arm connected!')
else:
    print ('Robotic arm not connected or offline!')

def Light():
    global light
    light = 1 - light
    RoboArm.ctrl_transfer(0x40,6,0x100,0,[0,0,light],3)

def AllOff():
    RoboArmOff = usb.core.find(idVendor=0x1267, idProduct=0x000)
    attemtps = 0
    while True:
        try:
            RoboArmOff.ctrl_transfer(0x40,6,0x100,0,[0,0,light],3)
            break
        except:
            if (attemtps == 0):
                print ('USB con error ... consider an emergency shutdown!')
            try:
                RoboArmOff = usb.core.find(idVendor=0x1267, idProduct=0x000)
            except:
                print ('Shit. Manual emergency shutdown required!')
            attemtps += 1
            if (attemtps == 20):
                break

def MoveArm(Duration, ArmCmd):
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,3)
    time.sleep(Duration)

def run(readable_results, data, rawbuf):
    if (len(readable_results) > 2 or len(readable_results) == 0):
        return
    if RoboArm is None:
        print ('Robotic arm not connected or offline!')
        return
    try:
        if ('rotate' in readable_results and 'right' in readable_results): # rotate right
            MoveArm(1, [0,1,light])
        elif ('rotate' in readable_results and 'left' in readable_results): # rotate left
            MoveArm(1, [0,2,light])
        elif ('shoulder' in readable_results and 'up' in readable_results): # shoulder up
            MoveArm(0.4, [64,0,light])
        elif ('shoulder' in readable_results and 'down' in readable_results): # shoulder down
            MoveArm(0.4, [128,0,light])
        elif ('elbow' in readable_results and 'up' in readable_results): # elbow up
            MoveArm(0.3, [16,0,light])
        elif ('elbow' in readable_results and 'down' in readable_results): # elbow down
            MoveArm(0.3, [32,0,light])
        elif ('wrist' in readable_results and 'up' in readable_results): # wrist up
            MoveArm(0.3, [4,0,light])
        elif ('wrist' in readable_results and 'down' in readable_results): # wrist down
            MoveArm(0.3, [8,0,light])
        elif ('finger' in readable_results and 'open' in readable_results): # finger open
            MoveArm(0.1, [2,0,light])
        elif ('finger' in readable_results and 'close' in readable_results): # finger close
            MoveArm(0.1, [1,0,light])
        elif (readable_results[0] == 'light'): # light on/off
            Light()
    except Exception as err:
        print err
    finally:
        AllOff()
