from flask import Flask, jsonify, make_response, request, redirect
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

app = Flask(__name__, static_url_path='')

def initialize_cache():
	cache.set("machine-is-stopped", {"solenoid": 0, "killswitch": 0}) #represents the machine state in the real world
	cache.set("user-state", USER_STATES["stressed"])
	cache.set("user-heartrate", 85)
	cache.set("user-eda-std", 5)
	cache.set("user-eda-mean", 10)


initialize_cache()

###############################
# Threading
###############################
def on_new_bitalino_data(new_eda_std, new_eda_mean):
	cache.set("user-eda-std", new_eda_std)
	cache.set("user-eda-mean", new_eda_mean)
	pub.sendMessage('classifier.set_eda', new_eda_std=new_eda_std, new_eda_mean=new_eda_mean)

def on_new_classification(new_class, eda_std, eda_mean):
	current_state = "normal"
	print "new class is " + str(new_class) 
	for state, value in USER_STATES.items():
		if value == new_class:
			current_state = state
			cache.set("user-state", value)
			cache.set("user-eda-std", eda_std)
			cache.set("user-eda-mean", eda_mean)

pub.subscribe(on_new_bitalino_data, 'bitalino.new_data')
pub.subscribe(on_new_classification, 'classifier.new_class')
bitalino_thread = bitalinoThread.Bitalino_Thread()
classifier_thread = classifier.Classifier_Thread()
bitalino_thread.start()
classifier_thread.start()
imp = electricImp.Imp

###############################
# URL endpoints
###############################
@app.route("/", methods=['GET'])
def index_page():
	return app.send_static_file('index.html')

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

@app.route("/eda", methods=['GET', 'POST'])
def set_eda():
	if request.method == 'GET':
		return jsonify({"eda_std": cache.get("user-eda-std"),"eda_mean": cache.get("user-eda-mean")})
	elif request.method == 'POST':
		pub.sendMessage('classifier.set_eda', new_eda_std=float(request.form['eda_std']), 
											  new_eda_mean=float(request.form['eda_mean']))
		return 'Updated eda'

@app.route("/status", methods=["GET"])
def get_status():
	return jsonify(
		{"adam": {"heartrate": cache.get("user-heartrate"), "state": cache.get("user-state"), "machine": "Band Saw"},
		"mayank": {"heartrate": 100, "state": 0, "machine": "Table Saw"},
		"nick": {"heartrate": 120, "state": 0, "machine": "Wood Lathe"},
		"tom": {"heartrate": 20, "state": 0, "machine": "Drill Press"},
		"victor": {"heartrate": 40, "state": 0, "machine": "Milling Machine"},
		"lesia": {"heartrate": 60, "state": 0, "machine": "Grinding Machine"}
		}
	)

if __name__ == "__main__":
	app.run(debug=True) #debug True auto restarts server on code change
