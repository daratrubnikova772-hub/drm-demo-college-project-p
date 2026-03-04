from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def load_key(filename):
    with open(filename, 'rb') as f:
        return f.read()

def encrypt_file(input_filepath, output_filepath, key):
    with open(input_filepath, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(output_filepath, 'wb') as f:
        f.write(encrypted)

def decrypt_file(input_filepath, output_filepath, key):
    with open(input_filepath, 'rb') as f:
        encrypted_data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)
    with open(output_filepath, 'wb') as f:
        f.write(decrypted)