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


# test if users table exists in users db
def test_users_table():
    os.system('python create_dbs.py')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "users table does not exist"

    # remove the dbs after test
    os.remove('users.db')
    os.remove('health.db')


# test if health table exists in health db
def test_health_table():
    os.system('python create_dbs.py')
    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='health';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "health table does not exist"
    
    # remove the dbs after test
    os.remove('users.db')
    os.remove('health.db')
