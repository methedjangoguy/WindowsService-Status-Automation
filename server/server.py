from flask import Flask, jsonify
from config.config import CHECK_RESULTS, configuration
import logging
import json
import os

_server_logger = logging.getLogger("server")

app = Flask(__name__)

CHECK_RESULTS_FILE = configuration.get_property("jsonfile")

def load_existing_checks():
    if os.path.exists(CHECK_RESULTS_FILE):
        with open(CHECK_RESULTS_FILE, 'r') as file:
            CHECK_RESULTS = json.load(file)
        # print("Loaded existing checks:", CHECK_RESULTS)
        return CHECK_RESULTS
    else:
        print("No existing checks file found.")

@app.route('/services', methods=['GET'])
def services():
    CR = load_existing_checks()
    # Check if there are any checks available before accessing the list
    if CR["checks"]:
        # Retrieve the latest services results if available
        return jsonify([result["services"] for result in CR["checks"]][-1])
    else:
        # Return an empty list or appropriate message when no checks have been performed yet
        return jsonify({"message": "No service checks have been performed yet"}),404


@app.route('/services/<servicename>', methods=['GET'])
def service(servicename):
    CR = load_existing_checks()
    if CR["checks"]:
        # Loop through the latest check to find the specified service
        for result in CR["checks"][-1]["services"]:
            if result["Servicename"].lower() == servicename.lower():
                return jsonify(result)
        return jsonify({"error": "Service not found"}), 404
    else:
        # Return an error message if no checks have been performed
        return jsonify({"error": "No checks have been performed yet"}), 404

def start_server():
    _server_logger.info(f"Server Started.")
    app.run(debug=True, use_reloader=False)