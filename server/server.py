from flask import Flask, jsonify, make_response, request
from werkzeug.contrib.cache import SimpleCache
from pubsub import pub
import time
import threading
import bitalinoThread
import classifier
import electricImp
import json


USER_STATES = classifier.USER_STATES

###############################
# Caching
###############################
cache = SimpleCache(default_timeout=99999999)
app = Flask(__name__)


def initialize_cache():
	cache.set("machine-is-stopped", {"solenoid": 0, "killswitch": 0}) #represents the machine state in the real world
	cache.set("user-state", USER_STATES["normal"])
	cache.set("user-heartrate", 85)

initialize_cache()

###############################
# Threading
###############################
def on_new_bitalino_data(new_data):
	pub.sendMessage('classifier.new_eda_measurement', new_reading=5)

def on_new_classification(new_class, heartrate=0):
	current_state = "normal"
	for state, value in USER_STATES.items():
		if value == new_class:
			current_state = state
			cache.set("user-state", value)
			cache.set("user-heartrate", heartrate)
			print "User is now class " + state

pub.subscribe(on_new_bitalino_data, 'bitalino.new_data')
pub.subscribe(on_new_classification, 'classifier.new_class')
bitalino_thread = bitalinoThread.Bitalino_Thread()
classifier_thread = classifier.Classifier_Thread()
bitalino_thread.start()
classifier_thread.start()

imp = electricImp.Imp
print "Server still works with Bitalino error plz stawp"
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
	response = make_response("")
	if request.method == 'GET':
		imp_status=json.loads(imp.get_state().read())
		cache.set("machine-is-stopped", imp_status)
		response = make_response(jsonify(cache.get("machine-is-stopped")))
	elif request.method == 'POST':
		data = request.get_json()
		imp.send_state(data['stopped'])
		imp_status=json.loads(imp.get_state().read())
		cache.set("machine-is-stopped", imp_status)
		response = make_response(jsonify(cache.get("machine-is-stopped")))
	response.headers['Access-Control-Allow-Origin'] = "*"
	return response

@app.route("/heartrate", methods=['GET', 'POST'])
def update_heartrate():
	if request.method == 'GET':
		return jsonify({"heartrate": cache.get("user-heartrate")})
	elif request.method == 'POST':
		pub.sendMessage('classifier.new_heart_rate', new_rate=float(request.form['rate']))
		return 'Updated heart rate'

@app.route("/status", methods=["GET"])
def get_status():
	return jsonify(
		{"adam": {"heartrate": cache.get("user-heartrate"), "state": cache.get("user-state"), "machine": "Bandsaw"},
		"mayank": {"heartrate": 100, "state": 0, "machine": "Sex LOL"},
		"nick": {"heartrate": 120, "state": 1, "machine": "Generic Mill 101"},
		"tom": {"heartrate": 20, "state": 2, "machine": "Drillpress"},
		"victor": {"heartrate": 40, "state": 0, "machine": "O O O O"},
		"lesia": {"heartrate": 60, "state": 0, "machine": "Mayank"}
		}
	)

if __name__ == "__main__":
	app.run(debug=True) #debug True auto restarts server on code change