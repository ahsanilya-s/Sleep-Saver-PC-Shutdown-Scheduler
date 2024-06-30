from flask import Flask, request, jsonify, send_from_directory
import os
import time
import threading

app = Flask(__name__, static_folder='static')

shutdown_thread = None
shutdown_time = 0

def shutdown_computer(delay):
    global shutdown_time
    while delay > 0 and shutdown_thread:
        time.sleep(1)
        delay -= 1
        shutdown_time = delay
    if shutdown_thread:
        os.system("shutdown /s /t 1")

@app.route('/schedule_shutdown', methods=['POST'])
def schedule_shutdown():
    global shutdown_thread, shutdown_time
    data = request.json
    minutes = data.get('minutes')
    if not minutes:
        return jsonify({"error": "Minutes not provided"}), 400
    
    delay = minutes * 60
    shutdown_time = delay
    shutdown_thread = threading.Thread(target=shutdown_computer, args=(delay,))
    shutdown_thread.start()
    
    return jsonify({"message": f"Shutdown scheduled in {minutes} minutes"}), 200

@app.route('/cancel_shutdown', methods=['POST'])
def cancel_shutdown():
    global shutdown_thread
    shutdown_thread = None
    os.system("shutdown /a")
    return jsonify({"message": "Shutdown cancelled"}), 200

@app.route('/get_remaining_time', methods=['GET'])
def get_remaining_time():
    return jsonify({"remaining_time": shutdown_time}), 200

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
