import pytest
import os 
from cryptography.fernet import Fernet


# test to see if the encryption key file exists 
def test_key_file_exists():
    os.system('python gen_key.py')
    assert os.path.exists('encryption.key')

    # remove the encrpytion key after test
    os.remove('encryption.key')

# test to see if the encryption key is the correct length (44 characters, fernet)
def test_key_length():
    os.system('python gen_key.py')
    with open('encryption.key', 'rb') as f:
        key = f.read()
    assert len(key) == 44
    
    # remove the encrpytion key after test
    os.remove('encryption.key')

