from flask import Flask, request, jsonify, render_template
import subprocess
import os
import atexit

app = Flask(__name__)

# Global variable to store the process and its PID
script_process = None

def shutdown_hook():
    global script_process
    if script_process:
        script_process.terminate()
        script_process = None
        print("process terminated")

# Register the shutdown hook to ensure the script is terminated on app shutdown
atexit.register(shutdown_hook)

@app.route('/')
def index():
    # Check if the script is running
    pid = None
    if script_process:
        pid = script_process.pid
    return render_template('index.html', pid=pid)

@app.route('/start', methods=['POST'])
def start_script():
    global script_process
    if script_process is not None:
        return jsonify({'status': 'Script is already running', 'pid': script_process.pid}), 400

    # Start the script in a new subprocess
    script_process = subprocess.Popen(['python', 'main.py'])
    return jsonify({'status': 'Script started successfully', 'pid': script_process.pid}), 200

@app.route('/stop', methods=['POST'])
def stop_script():
    global script_process
    if script_process is None:
        return jsonify({'status': 'No script is running'}), 400

    # Terminate the script process
    pid = script_process.pid
    script_process.terminate()
    script_process = None
    return jsonify({'status': 'Script stopped successfully', 'pid': pid}), 200

if __name__ == '__main__':
    app.run(debug=True)
