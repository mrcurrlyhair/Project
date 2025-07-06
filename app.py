from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
import hashlib

app = Flask(__name__, static_folder='static')
app.secret_key = 'Winston1'


# hashing function 
def hashing_pass(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()


# SQLite user connection
def userdb_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# SQLite health connection
def healthdb_connection():
    conn = sqlite3.connect('health.db')
    conn.row_factory = sqlite3.Row
    return conn


# home/landing page
@app.route('/')
def home():
    return render_template('home.html')

# information page
@app.route('/information')
def information():
    return render_template('information.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hashing_pass(request.form['password'])

        conn = userdb_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('account'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

# sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hashing_pass(request.form['password'])

        try:
            # add user to users.db
            conn_user = userdb_connection()
            cursor = conn_user.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn_user.commit()

            # get user_id
            user_id = cursor.lastrowid
            conn_user.close()

            # add user to health.db with that user_id
            conn_health = healthdb_connection()
            conn_health.execute('INSERT INTO health (user_id) VALUES (?)', (user_id,))
            conn_health.commit()
            conn_health.close()

            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = 'Username already taken'

    return render_template('signup.html', error=error)

# account view page
@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('account.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# delete account for patient 
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' in session:
        user_id = session['user_id']

        # delete from health.db
        conn_health = healthdb_connection()
        conn_health.execute('DELETE FROM health WHERE user_id = ?', (user_id,))
        conn_health.commit()
        conn_health.close()

        # delete from users.db
        conn_user = userdb_connection()
        conn_user.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn_user.commit()
        conn_user.close()

        session.clear()
        flash('Your account was deleted successfully')

    return redirect(url_for('home'))

# funtion to get current users health record
def get_health(user_id):
    conn = healthdb_connection()
    record = conn.execute('SELECT * FROM health WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return record

# medical records page
@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = healthdb_connection()

    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        county_name = request.form['county_name']
        smoking_status = request.form['smoking_status']
        alcohol_use = request.form['alcohol_use']
        physical_activity = request.form['physical_activity']
        diet_quality = request.form['diet_quality']
        sleep_hours = request.form['sleep_hours']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = round(weight / (height / 100) ** 2, 1)

        # update the user records in health db
        conn.execute('''
            UPDATE health SET
                age = ?, gender = ?, county_name = ?, smoking_status = ?, alcohol_use = ?,
                physical_activity = ?, diet_quality = ?, sleep_hours = ?, BMI = ?
            WHERE user_id = ?
        ''', (age, gender, county_name, smoking_status, alcohol_use,
              physical_activity, diet_quality, sleep_hours, bmi, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('medical_records'))

    # get current health data
    record = conn.execute('SELECT * FROM health WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    edit = request.args.get('edit') == 'true'

    return render_template('medical_records.html', record=record, edit=edit)

@app.route('/predictor')
def predictor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('predictor.html')



if __name__ == '__main__':
    app.run(debug=True)
