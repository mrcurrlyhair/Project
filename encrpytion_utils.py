from cryptography.fernet import Fernet

with open('secret.key', 'rb') as f:
    key = f.read()

cipher = Fernet(key)

# encrypt data
def encrypt_data(data):
    if data is None:
        return None
    return cipher.encrypt(str(data).encode('utf-8'))

# decrypt data
def decrypt_data(data):
    if data is None:
        return None
    return cipher.decrypt(data).decode('utf-8')
