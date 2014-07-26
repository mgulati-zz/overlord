import bitalino
import numpy
import threading
from pubsub import pub

MAC_ADDRESS = "98:d3:31:b2:13:9a" #aa is the other groups. 9a is ours
SAMPLING_RATE = 100
BITALINO_PORTS = {"EDA": 3}

class Bitalino_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 0
		self.name = "Bitalino Connection"
		self.deviations = []

	def run(self):
		self.device = bitalino.BITalino(MAC_ADDRESS)
		print "Connecting to Bitalino at " + MAC_ADDRESS
		self.device.start(SAMPLING_RATE, [ BITALINO_PORTS["EDA"] ])
		print "Done Connecting"
		self.previous_mean = 0
		for i in xrange(0,50):
		 	self.take_reading(5*SAMPLING_RATE)
		print self.deviations

	def take_reading(self, samples):
		self.device.trigger([0,0,1,0]) #digi 2 is the LED
		data = self.device.read(samples)
		print data
		eda_reading = data[:,5]
		self.device.trigger([0,0,0,0])
		net_deviance = self.previous_mean * numpy.nanstd(eda_reading)
		deviation = numpy.nanstd(eda_reading)
		if deviation > 45:
			print "greater than 45"
		self.deviations.append(deviation) #nanstd ignores NaNs in case our data is borked
		pub.sendMessage('bitalino.new_data', new_eda_std=deviation, new_eda_mean=self.previous_mean)
		self.previous_mean = numpy.mean(eda_reading)

	def cleanup(self):
		stopped = self.device.stop()
		if (stopped):
			print "Stopped Successfully"
		else:
			print "Failed to Stop Bitalino Acquisition"