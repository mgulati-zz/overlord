import numpy
import threading
import time
from pubsub import pub

USER_STATES = {"normal": 0, "fatigued": 1, "stressed": 2}
HEART_RATE_NORMALIZATION_FACTOR = 140.0 #the maximum heartrate recorded in test data
EDA_NORMALIZATION_FACTOR = 10.0 #maximum EDA reading in test data
TIME_NORMALIZATION_FACTOR = 10800.0 #maximum time at a machine (3 hours for now)

class Classifier_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = "Classification Worker"
		self.heartrate = 80/HEART_RATE_NORMALIZATION_FACTOR #BPM/normalization
		self.start_time = time.time()
		self.eda_reading = 0
		self.machine_weight = 0.5 #represents the relative risk of the machine
		self.current_state = USER_STATES["normal"]

	def run(self):
		pub.subscribe(self.set_heart_rate, "classifier.new_heart_rate")
		pub.subscribe(self.set_eda_reading, "classifier.new_eda_measurement")

	def set_heart_rate(self, new_rate):
		self.heartrate = new_rate/HEART_RATE_NORMALIZATION_FACTOR
		self.classify_current_user()

	def set_eda_reading(self, new_reading):
		print "setting EDA reading to " + str(new_reading)
		self.eda_reading = new_reading/EDA_NORMALIZATION_FACTOR
		self.classify_current_user()

	def classify_current_user(self):
		print "Classifying:\n     Heart: " + str(self.heartrate) +"\n     EDA: " + str(self.eda_reading)
		pub.sendMessage('classifier.new_class', new_class=self.current_state, heartrate=self.heartrate*HEART_RATE_NORMALIZATION_FACTOR)

def classify_user(heart_rate, eda_variance, normalized_time, machine_weight):
	#do something
	return 0