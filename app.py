from flask import Flask, jsonify, render_template
import subprocess
import os
import sys
import signal
import atexit

app = Flask(__name__)

# File to store the PID
PID_FILE = 'pid'

def read_pid():
    """Read the PID from the PID file."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as file:
            pid = file.read().strip()
            return int(pid) if pid else None
    return None

def write_pid(pid):
    """Write the PID to the PID file."""
    with open(PID_FILE, 'w') as file:
        file.write(str(pid))

def clear_pid():
    """Clear the PID file."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def terminate_script():
    """Terminate the script if it's running and clear the PID file."""
    pid = read_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
        clear_pid()
        print("\nScript Terminated")

atexit.register(terminate_script)

@app.route('/')
def index():
    pid = read_pid()
    return render_template('index.html', pid=pid)

@app.route('/start', methods=['POST'])
def start_script():
    if read_pid() is not None:
        return jsonify({'status': 'Script is already running'}), 400

    # Use the current Python executable to run the script
    python_path = sys.executable
    script_process = subprocess.Popen([python_path, 'main.py'])
    write_pid(script_process.pid)
    return jsonify({'status': 'Script started successfully', 'pid': script_process.pid}), 200

@app.route('/stop', methods=['POST'])
def stop_script():
    pid = read_pid()
    if pid is None:
        return jsonify({'status': 'No script is running'}), 400

    try:
        os.kill(pid, signal.SIGTERM)
        clear_pid()
    except OSError:
        return jsonify({'status': 'Failed to stop the script'}), 500

    return jsonify({'status': 'Script stopped successfully', 'pid': pid}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
