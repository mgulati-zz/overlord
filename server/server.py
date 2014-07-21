from flask import Flask
from flask import request
from werkzeug.contrib.cache import SimpleCache
from pubsub import pub
import time
import threading
import bitalinoThread
import classifier

USER_STATES = classifier.USER_STATES

###############################
# Caching
###############################
cache = SimpleCache()
app = Flask(__name__)


def initialize_cache():
	cache.set("machine-is-stopped", 'false') #represents the machine state in the real world
	cache.set("user-state", USER_STATES["normal"])

initialize_cache()

###############################
# Threading
###############################
def on_new_bitalino_data(new_data):
	pub.sendMessage('classifier.new_eda_measurement', new_reading=5)

def on_new_classification(new_class):
	current_state = "normal"
	for state, value in USER_STATES.items():
		if value == new_class:
			current_state = state
	print "User is now class " + state

pub.subscribe(on_new_bitalino_data, 'bitalino.new_data')
pub.subscribe(on_new_classification, 'classifier.new_class')
bitalino_thread = bitalinoThread.Bitalino_Thread()
classifier_thread = classifier.Classifier_Thread()
bitalino_thread.start()
classifier_thread.start()

###############################
# URL endpoints
###############################
@app.route("/", methods=['GET', 'POST'])
def index_page():
	if request.method == 'POST':
		return "This is what Lesia needs"
	else:
		return "Under Funstruction"

@app.route("/stop", methods=['GET', 'POST'])
def update_stopped_status():
	if request.method == 'GET':
		return cache.get("machine-is-stopped")
	elif request.method == 'POST':
		cache.set("machine-is-stopped", request.form['stopped'])
		return cache.get("machine-is-stopped")

@app.route("/heartrate", methods=['GET', 'POST'])
def update_heartrate():
	if request.method == 'GET':
		return "Not Yet Implemented" #implement pls
	elif request.method == 'POST':
		pub.sendMessage('classifier.new_heart_rate', request.form['rate'])
		return 'Updated heart rate'


if __name__ == "__main__":
	app.run(debug=False) #debug True auto restarts server on code change