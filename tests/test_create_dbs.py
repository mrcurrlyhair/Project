import pytest
import os 
import sqlite3

# test if users.db and health.db are created
def test_db_files_exist():
    os.system('python create_dbs.py')
    assert os.path.exists('users.db'), "users.db not found"
    assert os.path.exists('health.db'), "health.db not found"

    # remove the dbs after test
    os.remove('users.db')
    os.remove('health.db')


