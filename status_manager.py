import json
import os
from datetime import datetime

STATUS_FILE = "data/status.json"

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_status(status_data):
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)

def update_platform_status(platform, success, error_msg=""):
    status_data = load_status()
    if platform not in status_data:
        status_data[platform] = {
            "status": "HEALTHY",
            "consecutive_failures": 0,
            "last_success": None,
            "last_run": None,
            "last_error": ""
        }
    
    p_status = status_data[platform]
    p_status["last_run"] = datetime.now().isoformat()
    
    if success:
        p_status["status"] = "HEALTHY"
        p_status["consecutive_failures"] = 0
        p_status["last_success"] = p_status["last_run"]
        p_status["last_error"] = ""
    else:
        p_status["consecutive_failures"] += 1
        p_status["last_error"] = error_msg
        if p_status["consecutive_failures"] >= 5:
            p_status["status"] = "FAILED"
            
    save_status(status_data)

def reset_platform(platform):
    status_data = load_status()
    if platform in status_data:
        status_data[platform] = {
            "status": "HEALTHY",
            "consecutive_failures": 0,
            "last_success": status_data[platform].get("last_success"),
            "last_run": datetime.now().isoformat(),
            "last_error": "MANUALLY_RESET"
        }
        save_status(status_data)
        return True
    return False
