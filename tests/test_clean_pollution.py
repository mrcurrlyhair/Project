import pytest
import os
import pandas as pd

# test clean_pollution.py output
def test_clean_pollution():
    os.system('python clean_pollution.py')

    # check if the file exists 
    assert os.path.exists('CSVs/clean_pollution.csv')

    # load CSV 
    df = pd.read_csv('CSVs/clean_pollution.csv')

    # 108 counties check with no missing pollution levels
    assert len(df) == 108
    assert df['pollution_level'].notnull().all()

    # delete clean_pollution after test 
    os.remove('CSVs/clean_pollution.csv')