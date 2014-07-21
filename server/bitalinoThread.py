import bitalino
import numpy
import threading

MAC_ADDRESS = "98:d3:31:b2:13:9a"
SAMPLING_RATE = 10
BITALINO_PORTS = {"EMG": 0, "EDA": 1, "ECG": 2}


class Bitalino_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 0
		self.name = "Bitalino Thread"

	def run(self):
		self.device = bitalino.BITalino()
		print "Connecting to Bitalino at " + MAC_ADDRESS
		self.device.open(MAC_ADDRESS, SamplingRate = SAMPLING_RATE)
		self.device.start([ BITALINO_PORTS["EDA"] ])
		print "Done Connecting"
		self.take_reading(50)

	def take_reading(self, samples):
		print "hit"
		data = self.device.read(samples)
		print data