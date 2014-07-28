import numpy
import threading
import time
from pubsub import pub

USER_STATES = {"normal": 0, "fatigued": 1, "stressed": 2}
HEART_RATE_NORMALIZATION_FACTOR = 140.0 #the maximum heartrate recorded in test data
EDA_NORMALIZATION_FACTOR = 1.8 * 920 #Average standard deviation * maximum EDA reading in test data
TIME_NORMALIZATION_FACTOR = 10800.0 #maximum time at a machine (3 hours for now)
AGE_NORMALIZATION_FACTOR = 10000

class Classifier_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = "Classification Worker"
		self.heartrate = 80 #BPM
		self.start_time = time.time()
		self.eda_std = 5
		self.eda_mean = 10
		self.age = 20
		self.machine_weight = 0.5 #represents the relative risk of the machine
		self.current_state = USER_STATES["stressed"]

	def run(self):
		pub.subscribe(self.set_heart_rate, "classifier.new_heart_rate")
		pub.subscribe(self.set_eda, "classifier.set_eda")

	def set_heart_rate(self, new_rate):
		self.heartrate = new_rate
		self.classify_current_user()

	def set_eda(self, new_eda_std, new_eda_mean):
		self.eda_std = new_eda_std
		self.eda_mean = new_eda_mean
		self.classify_current_user()

	def classify_current_user(self):
		heartrate_factor = (self.heartrate+self.age/AGE_NORMALIZATION_FACTOR)/HEART_RATE_NORMALIZATION_FACTOR
		eda_factor = self.eda_std*self.eda_mean/EDA_NORMALIZATION_FACTOR
		fitness_factor = numpy.sqrt(heartrate_factor**2+eda_factor**2)
		print 'fitness_factor is ' + str(fitness_factor)
		if fitness_factor<0.5:
			self.current_state=USER_STATES["fatigued"]
		elif fitness_factor>3:
			self.current_state=USER_STATES["stressed"]
		else:
			self.current_state=USER_STATES["normal"]

		pub.sendMessage('classifier.new_class', new_class=self.current_state, eda_std=self.eda_std, eda_mean=self.eda_mean, fitness_factor=self.fitness_factor)

def classify_user(heart_rate, eda_variance, normalized_time, machine_weight):
	#do something
	return 0
