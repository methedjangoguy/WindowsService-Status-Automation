from config.config import configuration
import win32serviceutil
import win32service

def get_service_status(service_name):
    try:
        status = win32serviceutil.QueryServiceStatus(service_name)[1]
        if status == win32service.SERVICE_STOPPED:
            return "Stopped"
        else:
            return "Running"
    except Exception as e:
        print(f"Error getting status for {service_name}: {str(e)}")
        return "Error"