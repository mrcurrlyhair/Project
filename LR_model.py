import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE


# making sure the folder for the models to be saved exists 
os.makedirs('saved_models', exist_ok=True)

# record f1 scores to compare
results = 'CSVs/results.csv' 

def f1_results(model_type, disease, f1, model_file):
    entry = {'Model': model_type, 'Disease': disease, 'F1 Score': f1, 'File': model_file}
    if not os.path.exists(results):
        df = pd.DataFrame([entry])
    else:
        df = pd.read_csv(results)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(results, index=False)


# define parameter grid for logistic regression
lr_para = { 
    'C': [0.01, 0.1, 1, 10],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear', 'saga']
}


# load cleaned dataset
data = pd.read_csv('CSVs/cleaned_train_data.csv')


# function to train logistic regression with hyperparameters
def train_lr(X, y, name):

    # split into training and testing 
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=28, stratify=y)

    # scale integer features 
    scaler = StandardScaler()
    number = ['AGE', 'BMI', 'sleep_hours', 'pollution', 'radon_level', 'Total Cholesterol']
    x_train[number] = scaler.fit_transform(x_train[number])
    x_test[number] = scaler.transform(x_test[number])

    # balance training data using smote
    smote = SMOTE(random_state=28)
    x_train_bal, y_train_bal = smote.fit_resample(x_train, y_train)

    # run gridsearch for logistic regression
    grid = GridSearchCV(
        LogisticRegression(random_state=28, max_iter=10000), 
        lr_para, 
        cv=3, 
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    grid.fit(x_train_bal, y_train_bal)

    # get best parameters for logistic regression
    best_model = grid.best_estimator_

    # make predictions (probability of disease 1)
    prob = best_model.predict_proba(x_test)[:, 1]
    pred = (prob >= 0.6).astype(int)
 
    # f1 and accuracy 
    report = classification_report(y_test, pred, output_dict=True)
    f1 = report['1']['f1-score']
    print(f'Logistic Regression for {name}')
    print(classification_report(y_test, pred), accuracy_score(y_test, pred))

    # save model
    model = f'saved_models/lr_{name.lower().replace(" ", "_")}_model.pkl'
    with open(model, 'wb') as f:
        pickle.dump(best_model, f)
    print(f'saved {name} lr model')

    # save results 
    f1_results('Logistic Regression', name, f1, model)


# features not included
drop_cols = ['PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE', 'ZIP']
X_nf = data.drop(columns=drop_cols)

# convert categorical data into binary 
X_nf = pd.get_dummies(X_nf, drop_first=False)


# train lr model for each 
train_lr(X_nf, data['diabetes'], 'Diabetes')
train_lr(X_nf, data['heart_disease'], 'Heart Disease')
train_lr(X_nf, data['stroke'], 'Stroke')
train_lr(X_nf, data['hypertension'], 'Hypertension')
train_lr(X_nf, data['asthma'], 'Asthma')
train_lr(X_nf, data['copd'], 'COPD')
train_lr(X_nf, data['lung_cancer'], 'Lung Cancer')
