from flask import Flask, jsonify
from config.config import configuration, CHECK_RESULTS
import logging

_server_logger = logging.getLogger("server")

app = Flask(__name__)

@app.route('/services', methods=['GET'])
def services():
    return jsonify([result["services"] for result in CHECK_RESULTS["checks"]][-1])

@app.route('/services/<servicename>', methods=['GET'])
def service(servicename):
    for result in CHECK_RESULTS["checks"][-1]["services"]:
        if result["Servicename"].lower() == servicename.lower():
            return jsonify(result)
    return jsonify({"error": "Service not found"}), 404

def start_server():
    _server_logger.info(f"Server Started.")
    app.run(debug=True, use_reloader=False)