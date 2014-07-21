from flask import Flask
from flask import request
from werkzeug.contrib.cache import SimpleCache
import time
import threading
import bitalinoThread
import classifier

USER_STATES = classifier.USER_STATES
cache = SimpleCache()
app = Flask(__name__)


def initialize_cache():
	cache.set("machine-is-stopped", 'false') #represents the machine state in the real world
	cache.set("user-state", USER_STATES["normal"])

initialize_cache()

bitalino_thread = bitalinoThread.Bitalino_Thread()
bitalino_thread.start()

#ROUTING
@app.route("/", methods=['GET', 'POST'])
def index_page():
	if request.method == 'POST':
		return "This is what Lesia needs"
	else:
		return "Under Funstruction"

@app.route("/stop", methods=['GET', 'POST'])
def stop_system():
	if request.method == 'GET':
		return cache.get("machine-is-stopped")
	else:
		cache.set("machine-is-stopped", request.form['stopped'])
		return cache.get("machine-is-stopped")


if __name__ == "__main__":
	app.run(debug=True)