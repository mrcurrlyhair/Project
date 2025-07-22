import pytest
import os 
import pandas as pd 
import pickle

# test models_all creates correct model files and results
def test_models_all():
    os.system('python models_all.py')

    # check if results csv exists
    assert os.path.exists('CSVs/results.csv')

    # Load results csv
    results = pd.read_csv('CSVs/results.csv')

    # expect results for 7 diseases
    diseases = ['diabetes', 'heart_disease', 'stroke', 'hypertension', 'asthma', 'copd', 'lung_cancer']
    for disease in diseases:
        assert disease.capitalize() in results['Disease'].values

    # check if 21 models are saved in saved_models
    saved_models_path = 'saved_models'
    saved_model_files = os.listdir(saved_models_path)
    assert len(saved_model_files) == 21, f"Expected 21 models in saved_models, found {len(saved_model_files)}"

    # check if 7 final models have been moved and saved in static/final_models
    final_models_path = 'static/final_models'
    final_model_files = os.listdir(final_models_path)
    assert len(final_model_files) == 7, f"Expected 7 final models, found {len(final_model_files)}"

# test if the final models can be loaded and have predict method
def test_load_models():
    final_models_path = 'static/final_models'
    final_model_files = os.listdir(final_models_path)

    for model_file in final_model_files:
        model_path = os.path.join(final_models_path, model_file)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        assert hasattr(model, 'predict')