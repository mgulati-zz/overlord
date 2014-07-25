import bitalino
import numpy
import threading
from pubsub import pub

MAC_ADDRESS = "98:d3:31:b2:13:9a" #aa is the other groups. 9a is ours
SAMPLING_RATE = 100
BITALINO_PORTS = {"EMG": 0, "EDA": 1, "ECG": 2, "ACC": 3, "LUX": 4, "ABAT": 5}


class Bitalino_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 0
		self.name = "Bitalino Connection"

	def run(self):
		self.device = bitalino.BITalino()
		print "Connecting to Bitalino at " + MAC_ADDRESS
		self.device.open(MAC_ADDRESS, SamplingRate = SAMPLING_RATE)
		self.device.start([ BITALINO_PORTS["EDA"] ])
		print "Done Connecting"
		# while True:
		# 	self.take_reading(50)
		self.take_reading(500)
		self.cleanup()

	def take_reading(self, samples):
		self.device.trigger([0,0,1,0]) #digi 2 is the LED
		data = self.device.read(samples)
		print data
		self.device.stop()
		print "Stopped. Trying another 5"
		data = self.device.read(5)
		print data
		eda_reading = data[5,:]
		self.device.trigger([0,0,0,0])
		print "Max: " + str(numpy.max(eda_reading))
		print "Min: " + str(numpy.min(eda_reading))
		print "Mean: " + str(numpy.mean(eda_reading))
		print "Standard Deviation: " + str(numpy.nanstd(eda_reading)) #nanstd ignores NaNs in case our data is borked
		pub.sendMessage('bitalino.new_data', new_data=eda_reading)

	def cleanup(self):
		stopped = self.device.stop()
		if (stopped):
			print "Stopped Successfully"
		else:
			print "Failed to Stop Bitalino Acquisition"