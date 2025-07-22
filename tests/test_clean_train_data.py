import pytest
import os
import pandas as pd 

# test clean_train_data.py output
def test_clean_train_data():
    os.system('python clean_train_data.py')

    # check if the file exists
    assert os.path.exists('CSVs/cleaned_train_data.csv')

    # load CSV
    df = pd.read_csv('CSVs/cleaned_train_data.csv')

    # disease columns to exist with no missing values
    disease_columns = ['diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer']
    for col in disease_columns:
        assert col in df.columns
        assert df[col].isin([0, 1]).all()

    # make sure feature columns exist and isnt empty 
    features = [
        'BMI', 'Total Cholesterol', 'AGE', 'Body Height', 'Body Weight', 'Heart rate', 'Respiratory rate',
        'Systolic Blood Pressure', 'Diastolic Blood Pressure', 'smoking_status', 'alcohol_use',
        'physical_activity', 'diet_quality', 'sleep_hours', 'county_name', 'radon_level', 'pollution'
    ]

    for feature in features:
        assert feature in df.columns
        assert df[feature].notnull().all()

    # remove the cleaned_train_data  after test
    os.remove('CSVs/cleaned_train_data.csv')
