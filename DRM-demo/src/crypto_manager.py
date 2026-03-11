import json
import os
import base64
from cryptography.fernet import Fernet

KEYS_FILE = 'keys.json'

def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f)

def create_key(name):
    key = Fernet.generate_key()
    keys = load_keys()
    keys[name] = base64.urlsafe_b64encode(key).decode('utf-8')
    save_keys(keys)
    return key

def get_key(name):
    keys = load_keys()
    key_b64 = keys.get(name)
    if key_b64:
        return base64.urlsafe_b64decode(key_b64.encode('utf-8'))
    return None

def delete_key(name):
    keys = load_keys()
    if name in keys:
        del keys[name]
        save_keys(keys)
        return True
    return False

def list_keys():
    return list(load_keys().keys())

# Дополняем для удобства выбора ключа по имени
def select_key():
    keys = list_keys()
    if not keys:
        print("Нет сохранённых ключей.")
        return None
    print("Доступные ключи:")
    for i, name in enumerate(keys):
        print(f"{i + 1}. {name}")
    choice = input("Выберите номер ключа: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(keys):
            return get_key(keys[index])
        else:
            print("Некорректный выбор.")
            return None
    except ValueError:
        print("Некорректный ввод.")
        return None