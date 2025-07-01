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

# target variable for stroke
y_st = data['stroke']

# drop unneeded columns for stroke
X_st = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_st = pd.get_dummies(X_st, drop_first=True)

# split into train and test 
x_train_st, x_test_st, y_train_st, y_test_st = train_test_split(X_st, y_st, test_size=0.2, random_state=28, stratify=y_st)

# scale numbers
x_train_st[number] = scaler.fit_transform(x_train_st[number])
x_test_st[number] = scaler.transform(x_test_st[number])

# balance training data using smote
x_train_st_bal, y_train_st_bal = smote.fit_resample(x_train_st, y_train_st)

# define and train Random Forest for stroke
rf_st_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_st_model.fit(x_train_st_bal, y_train_st_bal)

# predict
rf_st_prob = rf_st_model.predict_proba(x_test_st)[:, 1]
rf_st_prediction = (rf_st_prob >= 0.6).astype(int)

# results
print('Random Forest for Stroke')
print(classification_report(y_test_st, rf_st_prediction), accuracy_score(y_test_st, rf_st_prediction))

# save stroke model
with open('saved_models/rf_stroke_model.pkl', 'wb') as f:
    pickle.dump(rf_st_model, f)
print('saved stroke rf model')

# target variable for hypertension
y_ht = data['hypertension']

# drop unneeded columns for hypertension
X_ht = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_ht = pd.get_dummies(X_ht, drop_first=True)

# split into train and test 
x_train_ht, x_test_ht, y_train_ht, y_test_ht = train_test_split(X_ht, y_ht, test_size=0.2, random_state=28, stratify=y_ht)

# scale numbers
x_train_ht[number] = scaler.fit_transform(x_train_ht[number])
x_test_ht[number] = scaler.transform(x_test_ht[number])

# balance training data using smote
x_train_ht_bal, y_train_ht_bal = smote.fit_resample(x_train_ht, y_train_ht)

# define and train Random Forest for hypertension
rf_ht_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_ht_model.fit(x_train_ht_bal, y_train_ht_bal)

# predict
rf_ht_prob = rf_ht_model.predict_proba(x_test_ht)[:, 1]
rf_ht_prediction = (rf_ht_prob >= 0.6).astype(int)

# results
print('Random Forest for Hypertension')
print(classification_report(y_test_ht, rf_ht_prediction), accuracy_score(y_test_ht, rf_ht_prediction))

# save hypertension model
with open('saved_models/rf_hypertension_model.pkl', 'wb') as f:
    pickle.dump(rf_ht_model, f)
print('saved hypertension rf model')

# target variable for asthma
y_as = data['asthma']

# drop unneeded columns for asthma
X_as = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_as = pd.get_dummies(X_as, drop_first=True)

# split into train and test 
x_train_as, x_test_as, y_train_as, y_test_as = train_test_split(X_as, y_as, test_size=0.2, random_state=28, stratify=y_as)

# scale numbers
x_train_as[number] = scaler.fit_transform(x_train_as[number])
x_test_as[number] = scaler.transform(x_test_as[number])

# balance training data using smote
x_train_as_bal, y_train_as_bal = smote.fit_resample(x_train_as, y_train_as)

# define and train Random Forest for asthma
rf_as_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_as_model.fit(x_train_as_bal, y_train_as_bal)

# predict
rf_as_prob = rf_as_model.predict_proba(x_test_as)[:, 1]
rf_as_prediction = (rf_as_prob >= 0.6).astype(int)

# results
print('Random Forest for Asthma')
print(classification_report(y_test_as, rf_as_prediction), accuracy_score(y_test_as, rf_as_prediction))

# save asthma model
with open('saved_models/rf_asthma_model.pkl', 'wb') as f:
    pickle.dump(rf_as_model, f)
print('saved asthma rf model')

# target variable for copd
y_cp = data['copd']

# drop unneeded columns for copd
X_cp = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_cp = pd.get_dummies(X_cp, drop_first=True)

# split into train and test 
x_train_cp, x_test_cp, y_train_cp, y_test_cp = train_test_split(X_cp, y_cp, test_size=0.2, random_state=28, stratify=y_cp)

# scale numbers
x_train_cp[number] = scaler.fit_transform(x_train_cp[number])
x_test_cp[number] = scaler.transform(x_test_cp[number])

# balance training data using smote
x_train_cp_bal, y_train_cp_bal = smote.fit_resample(x_train_cp, y_train_cp)

# define and train Random Forest for copd
rf_cp_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_cp_model.fit(x_train_cp_bal, y_train_cp_bal)

# predict
rf_cp_prob = rf_cp_model.predict_proba(x_test_cp)[:, 1]
rf_cp_prediction = (rf_cp_prob >= 0.6).astype(int)

# results
print('Random Forest for COPD')
print(classification_report(y_test_cp, rf_cp_prediction), accuracy_score(y_test_cp, rf_cp_prediction))

# save copd model
with open('saved_models/rf_copd_model.pkl', 'wb') as f:
    pickle.dump(rf_cp_model, f)
print('saved copd rf model')

# target variable for lung cancer
y_lc = data['lung_cancer']

# drop unneeded columns for lung cancer
X_lc = data.drop(columns=[
    'PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE'
])

# ohe categorical features
X_lc = pd.get_dummies(X_lc, drop_first=True)

# split into train and test 
x_train_lc, x_test_lc, y_train_lc, y_test_lc = train_test_split(X_lc, y_lc, test_size=0.2, random_state=28, stratify=y_lc)

# scale numbers
x_train_lc[number] = scaler.fit_transform(x_train_lc[number])
x_test_lc[number] = scaler.transform(x_test_lc[number])

# balance training data using smote
x_train_lc_bal, y_train_lc_bal = smote.fit_resample(x_train_lc, y_train_lc)

# define and train Random Forest for lung cancer
rf_lc_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    class_weight={0: 1, 1: 1.5},
    random_state=28
)
rf_lc_model.fit(x_train_lc_bal, y_train_lc_bal)

# predict
rf_lc_prob = rf_lc_model.predict_proba(x_test_lc)[:, 1]
rf_lc_prediction = (rf_lc_prob >= 0.6).astype(int)

# results
print('Random Forest for Lung Cancer')
print(classification_report(y_test_lc, rf_lc_prediction), accuracy_score(y_test_lc, rf_lc_prediction))

# save lung cancer model
with open('saved_models/rf_lung_cancer_model.pkl', 'wb') as f:
    pickle.dump(rf_lc_model, f)
print('saved lung cancer rf model')
