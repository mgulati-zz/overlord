from flask import Flask, jsonify, render_template
from flask import request
from werkzeug.contrib.cache import SimpleCache
import time
import threading
#import bitalinoThread
import classifier

USER_STATES = classifier.USER_STATES
cache = SimpleCache()
app = Flask(__name__)

def user_state(bpm=100, stress=0):
	return {'bpm': bpm, 'stress': stress}

machines_stopped = {'drill': 'false', 'band': 'false', 'lathe': 'false', 'mill': 'false', 'saw': 'false', 'grinder': 'false'}
users = {'adam': user_state(),'nick': user_state(),'lesia': user_state(), 'mayank': user_state(),'tom': user_state(),'vic': user_state()}

def initialize_cache():
	cache.set("machine-stops", machines_stopped) #represents the machine state in the real world
	cache.set("user-states", users)

initialize_cache()

#bitalino_thread = bitalinoThread.Bitalino_Thread()
#bitalino_thread.start()

#ROUTING
@app.route("/", methods=['GET', 'POST'])
def index_page():
	if request.method == 'POST':
		return "This is what Lesia needs"
	else:
		return "Under Funstruction"
		
@app.route("/overview", methods=["GET"])
def overview():
	return render_template("index.html")

@app.route("/stop", methods=['GET', 'POST'])
def stop_system():
	if request.method == 'GET':
		return cache.get("machine-stops")
	else:
		cache.set("machine-stops", request.form['stopped'])
		return cache.get("machine-stops")

@app.route("/users", methods=['GET', 'POST'])
def user():
	if request.method == 'GET':
		return jsonify(cache.get("user-states"))
	else:
		states = cache.get("user-states")
		states[request.form['name']] = user_state(request.form['bpm'], request.form['stress'])
		cache.set("user-states", states)
		return jsonify(cache.get("user-states"))

if __name__ == "__main__":
	app.run(debug=True)