from cryptography.fernet import Fernet

# generate encryption key
key = Fernet.generate_key()

# save key
with open('encryption.key', 'wb') as f:
    f.write(key)

print("encryption key generated and saved to encryption.key")
