import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# model and save locations
models = 'static/final_models/'
graphresults = 'results/graphs/'
CSVresults = 'results/CSVs/'

# make sure directorys exist
os.makedirs(graphresults, exist_ok=True)
os.makedirs(CSVresults, exist_ok=True)

for model_file in os.listdir(models):
    if model_file.endswith('.pkl'):
        model_path = os.path.join(models, model_file)
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        features = model.feature_names_in_

        # rf / xgb feature importance
        if hasattr(model, 'feature_importances_'):
            values = model.feature_importances_
            label = 'Importance'

        # lr coefficients / feature importance
        elif hasattr(model, 'coef_'):
            values = np.abs(model.coef_[0])
            label = 'Importance'

        else:
            print(f"{model_file} No feature importances")
            continue

        # create dataframe for plot
        df = pd.DataFrame({'Feature': features, label: values})
        df = df.sort_values(by=label, ascending=False)

        # save CSV
        csv_path = os.path.join(CSVresults, model_file.replace('.pkl', '_importance.csv'))
        df.to_csv(csv_path, index=False)

        # plot graph
        plt.figure(figsize=(8, 5))
        plt.barh(df['Feature'][:10], df[label][:10])
        plt.gca().invert_yaxis()
        plt.title(f"Top 10 Features: {model_file.replace('.pkl', '').replace('_', ' ').title()}")
        plt.xlabel(label)
        plt.ylabel('Feature')
        plt.tight_layout()

        # save graph
        img_path = os.path.join(graphresults, model_file.replace('.pkl', '_importance.png'))
        plt.savefig(img_path)
        plt.show()

        print(f"Saved {img_path} and {csv_path}")
