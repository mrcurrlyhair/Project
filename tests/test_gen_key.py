import pytest
import os 
from cryptography.fernet import Fernet

def test_key_file_exists():
    os.system('python gen_key.py')
    assert os.path.exists('encryption.key')
    os.remove('encryption.key')

def test_key_length():
    os.system('python gen_key.py')
    with open('encryption.key', 'rb') as f:
        key = f.read()
    assert len(key) == 44
    os.remove('encryption.key')

