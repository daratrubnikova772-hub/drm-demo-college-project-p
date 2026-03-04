import os
from crypto_utils import generate_key, save_key, load_key, encrypt_file, decrypt_file
from license import verify_license

# Пути и файлы
INPUT_FILE = 'input/контент.txt'
ENCRYPTED_FILE = 'output/контент.encrypted'
DECRYPTED_FILE = 'output/контент_decrypted.txt'
KEY_FILE = 'data/keys/secret.key'

def initialize_environment():
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = generate_key()
        save_key(key, KEY_FILE)
        print("Ключ сгенерирован и сохранен.")
    else:
        key = load_key(KEY_FILE)
    return key

def main_menu():
    print("\n=== Меню управления DRM ===")
    print("1. Проверить лицензию и расшифровать файл")
    print("2. Зашифровать исходный файл")
    print("3. Сгенерировать новый ключ")
    print("4. Выйти")
    choice = input("Выберите действие (1-4): ")
    return choice

def main():
    initialize_environment()
    key = load_or_create_key()

    while True:
        choice = main_menu()

        if choice == '1':
            if verify_license():
                print("Лицензия подтверждена. Расшифровка файла...")
                try:
                    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, key)
                    print(f"Файл расшифрован: {DECRYPTED_FILE}")
                except Exception as e:
                    print(f"Ошибка расшифровки: {e}")
            else:
                print("Лицензия не подтверждена. Расшифровка невозможна.")
        elif choice == '2':
            print("Зашифровка исходного файла...")
            try:
                encrypt_file(INPUT_FILE, ENCRYPTED_FILE, key)
                print(f"Файл зашифрован: {ENCRYPTED_FILE}")
            except Exception as e:
                print(f"Ошибка шифрования: {e}")
        elif choice == '3':
            confirm = input("Вы уверены, что хотите сгенерировать новый ключ? Это перезапишет текущий. (да/нет): ")
            if confirm.lower() in ['да', 'yes', 'y']:
                key = generate_key()
                save_key(key, KEY_FILE)
                print("Новый ключ сгенерирован и сохранён.")
            else:
                print("Генерация нового ключа отменена.")
        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()