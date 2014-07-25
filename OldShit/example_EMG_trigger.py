# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 10:06:18 2013

@author: Priscila Alves

EMG trigger:
In this example, the muscles can be used to turn the led on.
Every time the EMG signal is higher than a defined threshold, the led turns on, otherwise is off.
 
"""

import bitalino #BITalino API
import numpy

#call the BITalino API
device = bitalino.BITalino()

import time
macAddress= "98:d3:31:b2:13:9a"
SamplingRate = 1000
nFrames = 100 #number of samples to read
threshold = 50 #threshold defined to turn the led on
acquisitionTime = 20 # seconds 

#connect do BITalino device
device.open(macAddress, SamplingRate = SamplingRate)
time.sleep(1)

#start acquisition on analog channel 0 (EMG)
device.start([0])
print "START"
acquireLoop = 0

while(acquireLoop != (acquisitionTime *SamplingRate)):
    #read samples
    dataAcquired = device.read(nFrames)
    #get EMG signal
    EMG = dataAcquired[5,:]
    #center the EMG signal baseline at zero, by subtracting its mean
	#calculate the mean value of the absolute of the EMG signal
    value = numpy.mean(abs(EMG-numpy.mean(EMG)))
    if value >= threshold:
        #turn digital ports on
        device.trigger([1,1,1,1])
    else:
        #turn digital ports off
        device.trigger([0,0,0,0])
    acquireLoop+=nFrames

#stop acquisition  
device.stop()
#diconnect device
device.close()
print "STOP"
        