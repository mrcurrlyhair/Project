import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# load cleaned dataset
data = pd.read_csv('CSVs/cleaned_data.csv')

# target variable
y = data['diabetes']

# drop unneeded columns
X = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X = pd.get_dummies(X, drop_first=True)

# split into train and test 
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=28, stratify=y)

# scale numbers
scaler = StandardScaler()
number = ['AGE', 'BMI', 'sleep_hours', 'pollution']
x_train[number] = scaler.fit_transform(x_train[number])
x_test[number] = scaler.transform(x_test[number])

# balance training data using smote
smote = SMOTE(random_state=28)
x_train_bal, y_train_bal = smote.fit_resample(x_train, y_train)

# define and train Random Forest
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_model.fit(x_train_bal, y_train_bal)

# predict
rf_prob = rf_model.predict_proba(x_test)[:, 1]
rf_prediction = (rf_prob >= 0.6).astype(int)

# results
print('Random Forest for Diabetes')
print(classification_report(y_test, rf_prediction), accuracy_score(y_test, rf_prediction))

# save model
os.makedirs('saved_models', exist_ok=True)
with open('saved_models/rf_diabetes_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print('saved diabetes rf model')

# target variable for heart disease
y_hd = data['heart_disease']

# drop unneeded columns for heart disease
X_hd = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_hd = pd.get_dummies(X_hd, drop_first=True)

# split into train and test 
x_train_hd, x_test_hd, y_train_hd, y_test_hd = train_test_split(X_hd, y_hd, test_size=0.2, random_state=28, stratify=y_hd)

# scale numbers
x_train_hd[number] = scaler.fit_transform(x_train_hd[number])
x_test_hd[number] = scaler.transform(x_test_hd[number])

# balance training data using smote
x_train_hd_bal, y_train_hd_bal = smote.fit_resample(x_train_hd, y_train_hd)

# define and train Random Forest for heart disease
rf_hd_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_hd_model.fit(x_train_hd_bal, y_train_hd_bal)

# predict
rf_hd_prob = rf_hd_model.predict_proba(x_test_hd)[:, 1]
rf_hd_prediction = (rf_hd_prob >= 0.6).astype(int)

# results
print('Random Forest for Heart Disease')
print(classification_report(y_test_hd, rf_hd_prediction), accuracy_score(y_test_hd, rf_hd_prediction))

# save heart disease model
with open('saved_models/rf_heart_disease_model.pkl', 'wb') as f:
    pickle.dump(rf_hd_model, f)
print('saved heart disease rf model')
