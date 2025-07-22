import pytest
import os
import pandas as pd

# test clean_pollution.py output
def test_clean_pollution():
    os.system('python clean_pollution.py')
    assert os.path.exists('CSVs/clean_pollution.csv')

    df = pd.read_csv('CSVs/clean_pollution.csv')

    # 108 counties check
    assert len(df) == 108
    assert df['pollution_level'].notnull().all()

    # delete clean_pollution after test 
    os.remove('CSVs/clean_pollution.csv')