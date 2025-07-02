import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# define parameter grid for logistic regression
lr_para = { 
    'C': [0.01, 0.1, 1, 10],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear', 'saga']
}

# load cleaned dataset
data = pd.read_csv('CSVs/cleaned_data.csv')

# function to train logistic regression with hyperparameters
def train_lr(X, y, name):
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=28, stratify=y)

    scaler = StandardScaler()
    number = ['AGE', 'BMI', 'sleep_hours', 'pollution', 'radon_level']
    x_train[number] = scaler.fit_transform(x_train[number])
    x_test[number] = scaler.transform(x_test[number])

    smote = SMOTE(random_state=28)
    x_train_bal, y_train_bal = smote.fit_resample(x_train, y_train)

    grid = GridSearchCV(
        LogisticRegression(random_state=28, max_iter=15000), 
        lr_para, 
        cv=3, 
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    grid.fit(x_train_bal, y_train_bal)
    best_model = grid.best_estimator_

    prob = best_model.predict_proba(x_test)[:, 1]
    pred = (prob >= 0.6).astype(int)

    print(f'Logistic Regression for {name}')
    print(classification_report(y_test, pred), accuracy_score(y_test, pred))

    with open(f'saved_models/lr_{name.lower().replace(" ", "_")}_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print(f'saved {name} logistic regression model')


# features not included
drop_cols = ['PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE']
X_nf = data.drop(columns=drop_cols)
X_nf = pd.get_dummies(X_nf, drop_first=True)

# train each disease model
train_lr(X_nf, data['diabetes'], 'Diabetes')
train_lr(X_nf, data['heart_disease'], 'Heart Disease')
train_lr(X_nf, data['stroke'], 'Stroke')
train_lr(X_nf, data['hypertension'], 'Hypertension')
train_lr(X_nf, data['asthma'], 'Asthma')
train_lr(X_nf, data['copd'], 'COPD')
train_lr(X_nf, data['lung_cancer'], 'Lung Cancer')
