import os
from crypto_utils import generate_key, save_key, load_key, encrypt_file, decrypt_file
from license_utils import create_license, verify_license, activate_license, load_licenses

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
    if os.path.exists(KEY_FILE):
        return load_key(KEY_FILE)
    else:
        print("Ключ не найден. Создайте новый ключ.")
        return None

def main_menu():
    print("\n=== Меню управления DRM и лицензиями ===")
    print("1. Проверить лицензию и расшифровать файл")
    print("2. Зашифровать исходный файл")
    print("3. Сгенерировать новый ключ")
    print("4. Создать новую лицензию")
    print("5. Проверить лицензию по ID")
    print("6. Активировать лицензию по ID")
    print("7. Выйти")
    choice = input("Выберите действие (1-7): ")
    return choice

def main():
    initialize_environment()
    key = load_or_create_key()

    while True:
        choice = main_menu()

        if choice == '1':
            license_id = input("Введите ID лицензии для проверки и расшифровки: ").strip()
            if verify_license(license_id):
                print("Лицензия действительна. Расшифровка файла...")
                try:
                    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, key)
                    print(f"Файл расшифрован: {DECRYPTED_FILE}")
                except Exception as e:
                    print(f"Ошибка расшифровки: {e}")
            else:
                print("Лицензия недействительна или истекла.")
        elif choice == '2':
            print("Зашифровка исходного файла...")
            try:
                encrypt_file(INPUT_FILE, ENCRYPTED_FILE, key)
                print(f"Файл зашифрован: {ENCRYPTED_FILE}")
            except Exception as e:
                print(f"Ошибка шифрования: {e}")
        elif choice == '3':
            confirm = input("Вы уверены, что хотите сгенерировать новый ключ? (да/нет): ").lower()
            if confirm in ['да', 'y', 'yes']:
                key = generate_key()
                save_key(key, KEY_FILE)
                print("Новый ключ сгенерирован и сохранён.")
            else:
                print("Генерация отменена.")
        elif choice == '4':
            user_name = input("Введите имя пользователя: ")
            product_name = input("Введите название продукта: ")
            days_valid = int(input("Введите количество дней действия лицензии: "))
            max_activations = int(input("Введите лимит активаций: "))
            license_data = create_license(user_name, product_name, days_valid, max_activations)
            print(f"Лицензия создана с ID: {license_data['license_id']}")
        elif choice == '5':
            license_id = input("Введите ID лицензии для проверки: ").strip()
            if verify_license(license_id):
                print("Лицензия действительна.")
            else:
                print("Лицензия недействительна или истекла.")
        elif choice == '6':
            license_id = input("Введите ID лицензии для активации: ").strip()
            activate_license(license_id)
        elif choice == '7':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()