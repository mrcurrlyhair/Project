import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# model location 
models = 'static/final_models/'

for model_file in os.listdir(models):
    if model_file.endswith('.pkl'):
        model_path = os.path.join(models, model_file)
        model = joblib.load(model_path)

        features = model.feature_names_in_

        #  rf xgb feature importance
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            values = importances
            label = 'Importance'

        # lr coefficients/feature importance
        elif hasattr(model, 'coef_'):
            coef = model.coef_[0]
            values = np.abs(coef)
            label = 'Importance'

        else:
            print(f"{model_file} No feature importances")
            continue

        # create dataframe for plot
        df = pd.DataFrame({'Feature': features, label: values})
        df = df.sort_values(by=label, ascending=False)

        # plot graph
        plt.figure(figsize=(8, 5))
        plt.barh(df['Feature'][:10], df[label][:10])
        plt.gca().invert_yaxis()
        plt.title(f'Top 10 Features: {model_file.replace(".pkl", "").replace("_", " ").title()}')
        plt.xlabel(label)
        plt.ylabel('Feature')
        plt.tight_layout()
        plt.show()
