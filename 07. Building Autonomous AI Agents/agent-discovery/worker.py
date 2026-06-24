from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

WORKER_ID = os.getenv('WORKER_ID', socket.gethostname())

@app.route('/status')
def status():
    """Return worker status"""
    return jsonify({
        "worker_id": WORKER_ID,
        "hostname": socket.gethostname(),
        "status": "healthy"
    })

@app.route('/process')
def process():
    """Simulate processing work"""
    return jsonify({
        "worker_id": WORKER_ID,
        "message": f"Task processed by {WORKER_ID}",
        "hostname": socket.gethostname()
    })

if __name__ == '__main__':
    print(f"🔧 Worker {WORKER_ID} starting...")
    print(f"   Hostname: {socket.gethostname()}")
    app.run(host='0.0.0.0', port=8000)
