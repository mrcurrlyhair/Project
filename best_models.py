import pandas as pd
import shutil


# load the results
results = pd.read_csv('CSVs/results.csv')

# go through each disease
for disease in results['Disease'].unique():
    results_disease = results[results['Disease'] == disease]
    best = results_disease.loc[results_disease['F1 Score'].idxmax()]

    shutil.copy(best['File'], 'static/final_models/')

    print(f"model for {disease} ({best['Model']}, F1: {best['F1 Score']:.2f}) copied")
