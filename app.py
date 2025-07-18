from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import pandas as pd
import joblib 
import os
from cryptography.fernet import Fernet
import re

app = Flask(__name__, static_folder='static')
app.secret_key = 'Winston1'


# hashing function 
def hashing_pass(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()

# load encryption key
with open('encryption.key', 'rb') as f:
    encryption_key = f.read()

encrypt = Fernet(encryption_key)

# encryption function
def encrypt_data(text):
    if text is None:
        return None
    return encrypt.encrypt(str(text).encode()).decode()

# decryption function
def decrypt_data(token):
    if token is None:
        return None
    return encrypt.decrypt(token.encode()).decode()


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
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

# sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'][:32]  
        password = request.form['password'][:32]  
        confirm_password = request.form['confirm_password'][:32]

        # hash password
        hashed_password = hashing_pass(password)

        # password requirements 
        password_requirements = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*\-])[A-Za-z\d!@#$%&*\-]{8,}$'

        # does both passwords match 
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('signup'))

        # check password strength
        if not re.match(password_requirements, password):
            flash("Password must be at least 8 characters, include an uppercase letter, a lowercase letter, a number, and a special character (!@#$%&*-).")
            return redirect(url_for('signup'))

        # does user already exist?
        conn_user = userdb_connection()
        cursor = conn_user.cursor()
        existing_user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            conn_user.close()
            flash("Username already exists. Please try again.")
            return redirect(url_for('signup'))

        # create user in users db
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn_user.commit()
        user_id = cursor.lastrowid
        conn_user.close()

        # create user in health db
        conn_health = healthdb_connection()
        conn_health.execute('INSERT INTO health (user_id) VALUES (?)', (user_id,))
        conn_health.commit()
        conn_health.close()

        flash("Account created successfully. Please log in.")
        return redirect(url_for('login'))

    return render_template('signup.html')


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

    # decrypt data
    if record:
        decrypted = {}
        for key in record.keys():
            value = record[key]
            if key in ['age', 'gender', 'county', 'smoking_status', 'alcohol_use', 'physical_activity', 
                       'diet_quality', 'sleep_hours', 'BMI', 'height', 'weight', 'heart_rate', 'respiratory_rate', 
                       'systolic_bp', 'diastolic_bp', 'radon_level', 'pollution_level', 'cholesterol']:
                decrypted[key] = decrypt_data(value)
            else:
                decrypted[key] = value
        return decrypted
    
    return None


# radon data
radon_data = pd.read_csv('CSVs/uk_radon.csv')
radon_lookup = dict(zip(radon_data['county'], radon_data['radon_level']))

# pollution data
pollution_data = pd.read_csv('CSVs/clean_pollution.csv')
pollution_lookup = dict(zip(pollution_data['county'], pollution_data['pollution_level']))


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
        county = request.form['county']
        smoking_status = request.form['smoking_status']
        alcohol_use = request.form['alcohol_use']
        physical_activity = request.form['physical_activity']
        diet_quality = request.form['diet_quality']
        sleep_hours = request.form['sleep_hours']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        heart_rate = float(request.form['heart_rate'])
        respiratory_rate = float(request.form['respiratory_rate'])
        systolic_bp = float(request.form['systolic_bp'])
        diastolic_bp = float(request.form['diastolic_bp'])
        cholesterol = float(request.form['cholesterol'])

        # calculate bmi
        bmi = round(weight / (height / 100) ** 2, 1)

        # get radon and pollution levels
        radon_level = radon_lookup.get(county, None)
        pollution_level = pollution_lookup.get(county, None)

        # save data and encrpyt
        conn.execute('''
            UPDATE health SET
                age = ?, gender = ?, county = ?, smoking_status = ?, alcohol_use = ?,
                physical_activity = ?, diet_quality = ?, sleep_hours = ?, BMI = ?,
                height = ?, weight = ?, heart_rate = ?, respiratory_rate = ?,
                systolic_bp = ?, diastolic_bp = ?, radon_level = ?, pollution_level = ?,
                cholesterol = ?
            WHERE user_id = ?
        ''', (
            encrypt_data(age), encrypt_data(gender), encrypt_data(county), encrypt_data(smoking_status), encrypt_data(alcohol_use),
            encrypt_data(physical_activity), encrypt_data(diet_quality), encrypt_data(sleep_hours), encrypt_data(bmi),
            encrypt_data(height), encrypt_data(weight), encrypt_data(heart_rate), encrypt_data(respiratory_rate),
            encrypt_data(systolic_bp), encrypt_data(diastolic_bp), encrypt_data(radon_level), encrypt_data(pollution_level),
            encrypt_data(cholesterol), user_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('medical_records'))

    
    record = conn.execute('SELECT * FROM health WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()

    # view and edit previous medical data
    decrypted_record = {}
    for key in record.keys():
        value = record[key]
        if key in ['age', 'gender', 'county', 'smoking_status', 'alcohol_use',
                   'physical_activity', 'diet_quality', 'sleep_hours', 'BMI',
                   'height', 'weight', 'heart_rate', 'respiratory_rate',
                   'systolic_bp', 'diastolic_bp', 'radon_level', 'pollution_level', 'cholesterol']:
            decrypted_record[key] = decrypt_data(value)
        else:
            decrypted_record[key] = value  

    edit = request.args.get('edit') == 'true'

    return render_template('medical_records.html', record=decrypted_record, edit=edit)


# funtion to get disease name from model name (model name can change depedning on results/ when ran )
def disease_name(filename):
    return filename.replace('.pkl', '').replace('_', ' ').title()

# predictor route 
@app.route('/predictor')
def predictor():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # get user id from session and corasponding health data for user
    user_id = session['user_id']
    conn = healthdb_connection()
    record = conn.execute('SELECT * FROM health WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()

    # no health data error
    if not record:
        flash("No health data found. Please fill in your medical records.")
        return redirect(url_for('medical_records'))

    # prepare user data
    user_health = pd.DataFrame([dict(record)])

    # decrypt data
    for key in user_health.columns:
        if key in ['age', 'gender', 'county', 'smoking_status', 'alcohol_use',
                   'physical_activity', 'diet_quality', 'sleep_hours', 'BMI',
                   'height', 'weight', 'heart_rate', 'respiratory_rate',
                   'systolic_bp', 'diastolic_bp', 'radon_level', 'pollution_level', 'cholesterol']:
            user_health.at[0, key] = decrypt_data(user_health.at[0, key])

    # name change for columns due to training data name different, also error for when medical data is incomplete
    try:
        user_health['Body Height'] = float(user_health['height'])
        user_health['Body Weight'] = float(user_health['weight'])
        user_health['Total Cholesterol'] = float(user_health['cholesterol'])
    except (TypeError, ValueError):
        flash("Your medical records are incomplete. Please update your health data before using the predictor.")
        return redirect(url_for('medical_records'))

    # remove unneeded columns
    user_health.drop(columns=['id', 'user_id', 'county', 'height', 'weight', 'cholesterol'], inplace=True, errors='ignore')
    user_health = pd.get_dummies(user_health, drop_first=True)

    # model location  
    models = os.path.join('static', 'final_models')

    predictions = []

    for filename in os.listdir(models):
        if filename.endswith('.pkl'):
            model_path = os.path.join(models, filename)
            model = joblib.load(model_path)

            expected_cols = model.feature_names_in_
            user_input = user_health.reindex(columns=expected_cols, fill_value=0)

            X = user_input

            # predict
            if hasattr(model, 'predict_proba'):
                prob = model.predict_proba(X)[0][1]

            else:
                prob = model.predict(X)[0]

            # risk factor explanation / most important featrue
            risk_factors = []

            if hasattr(model, 'coef_'):
                importance = model.coef_[0]

            elif hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_


            top_features = sorted(zip(expected_cols, importance), key=lambda x: abs(x[1]), reverse=True)[:2]

            for feature, imp in top_features:
                user_value = X.iloc[0][feature]
                if imp > 0 and user_value > 0:
                    risk_factors.append(feature.replace('_', ' ').title())

            if risk_factors:
                reason = "Your risk is increased due to " + " and ".join(risk_factors)
            else:
                reason = "No major risk factors detected"

            # result
            predictions.append({
                'disease': disease_name(filename),
                'probability': round(prob * 100, 1),
                'reason': reason
            })

    # sort by probability
    predictions.sort(key=lambda x: x['probability'], reverse=True)

    return render_template('predictor.html', predictions=predictions)


if __name__ == '__main__':
    app.run(debug=True)
