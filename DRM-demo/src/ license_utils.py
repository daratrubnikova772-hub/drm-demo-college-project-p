import json
import os
from datetime import datetime, timedelta
import hashlib

LICENSES_FILE = 'licenses.json'

def create_license(user_name, product_name, days_valid=365, max_activations=1):
    issue_date = datetime.now()
    expiry_date = issue_date + timedelta(days=days_valid)
    license_id = hashlib.sha256((user_name + product_name + str(issue_date)).encode()).hexdigest()
    license_data = {
        "license_id": license_id,
        "user": user_name,
        "product": product_name,
        "issue_date": issue_date.strftime("%Y-%m-%d"),
        "expiry_date": expiry_date.strftime("%Y-%m-%d"),
        "max_activations": max_activations,
        "activations": 0,
    }
    save_license(license_data)
    print(f"Лицензия создана: ID={license_id}")
    return license_data

def save_license(license_data):
    licenses = load_licenses()
    licenses[license_data["license_id"]] = license_data
    with open(LICENSES_FILE, 'w') as f:
        json.dump(licenses, f, indent=4)

def load_licenses():
    if os.path.exists(LICENSES_FILE):
        with open(LICENSES_FILE, 'r') as f:
            return json.load(f)
    return {}

def verify_license(license_id):
    licenses = load_licenses()
    license_data = licenses.get(license_id)
    if not license_data:
        print("Лицензия не найдена.")
        return False
    today = datetime.now()
    expiry_date = datetime.strptime(license_data["expiry_date"], "%Y-%m-%d")
    if today > expiry_date:
        print("Лицензия истекла.")
        return False
    if license_data["activations"] >= license_data["max_activations"]:
        print("Достигнут лимит активных устройств.")
        return False
    return True

def activate_license(license_id):
    licenses = load_licenses()
    if license_id in licenses:
        licenses[license_id]["activations"] += 1
        save_license(licenses[license_id])
        print(f"Лицензия {license_id} активирована.")
    else:
        print("Лицензия не найдена для активации.")