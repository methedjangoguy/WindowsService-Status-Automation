import log.log as log
from service.servicestatus import *
from config.config import configuration, CHECK_RESULTS, EMAIL_SENT_HISTORY
import json
import datetime
from emailworker.email import *
import time
import threading
from server.server import *
import os

_root_logger = log.setup_custom_logger("root")

CHECK_RESULTS_FILE = configuration.get_property("jsonfile")
SERVICES = configuration.get_property("services")
monitoring_interval = configuration.get_property("monitoring_interval")

def load_existing_checks():
    global CHECK_RESULTS
    if os.path.exists(CHECK_RESULTS_FILE):
        with open(CHECK_RESULTS_FILE, 'r') as file:
            CHECK_RESULTS = json.load(file)

def load_email_sent_history():
    # Load the last email sent times from the checks if available
    for check in CHECK_RESULTS.get('checks', []):
        for service in check.get('services', []):
            servicename = service.get('Servicename')
            last_email_sent = service.get('lastemailsent_time')
            if last_email_sent:
                EMAIL_SENT_HISTORY[servicename] = datetime.datetime.strptime(last_email_sent, "%Y-%m-%d %H:%M:%S")

def check_services():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    check_result = {"check_id": f"Check {len(CHECK_RESULTS['checks']) + 1}", "services": []}

    for service_name in SERVICES:
        status = get_service_status(service_name)
        email_sent = send_email(service_name)
        
        if email_sent:
            last_email_sent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_email_sent_time = EMAIL_SENT_HISTORY.get(service_name, "")
            if last_email_sent_time:
                last_email_sent_time = last_email_sent_time.strftime("%Y-%m-%d %H:%M:%S")

        service_result = {
            "Servicename": service_name,
            "Status": status,
            "lastchecked_time": now,
            "lastemailsent_time": last_email_sent_time
        }

        check_result["services"].append(service_result)

    CHECK_RESULTS["checks"].append(check_result)
    with open(CHECK_RESULTS_FILE, "w") as file:
        json.dump(CHECK_RESULTS, file, indent=4)

    next_check_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
    _root_logger.info(f'Service checks done. Next check in {monitoring_interval} seconds, at {next_check_time.strftime("%Y-%m-%d %H:%M:%S")}')

def main():
    _root_logger.info(f"Process Execution Started.\n")
    while True:
        check_services()
        time.sleep(monitoring_interval)
    _root_logger.info(f"Process Execution Ended.")
    
if __name__ == "__main__":
    load_existing_checks()
    load_email_sent_history()
    thread = threading.Thread(target=main)
    thread.start()
    start_server()
   
