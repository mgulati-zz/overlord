import bitalino
import numpy
import time
import csv
import time


device = bitalino.BITalino()
macAddress = "98:d3:31:b2:13:9a"
SamplingRate = 100 #Samples/Second
device.open(macAddress, SamplingRate = SamplingRate) # Set MAC address and sampling rate
time.sleep(1)

PORTS = {"EMG": 0, "ECG": 2}

device.start([PORTS["ECG"]])
name = raw_input("Enter Name: ")
fname = raw_input("Enter File Name: ")
numsamples = raw_input("How Many Samples: ")


outfile = open(fname + ".csv", "wb")
writer = csv.writer(outfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)

writer.writerow("Time," + name)

print "STARTED"

def baseline(vals):
	return numpy.mean(abs(vals-numpy.mean(vals)))

def cur_time():
	return int(round(time.time()))

def relative_time():
	return cur_time() - start_time

print "Alright man we're going!"

recorded = []
start_time = cur_time()
i=0
while i<numsamples:
	data = device.read(10)
	value = baseline(data[5,:])
	print "Sample " + str(i) +": " + str(value)
	writer.writerow(str(relative_time()) + "," + str(value))
	i += 1

print "Done"
outfile.close()

device.stop()

device.close()
time.sleep(3)
