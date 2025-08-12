import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support

# model and save locations
models = 'static/final_models/'
graphresults = 'results/graphs/'
CSVresults = 'results/CSVs/'
allmodels = 'saved_models/'
results = 'results/results.csv'

# make sure folders exist
os.makedirs(graphresults, exist_ok=True)
os.makedirs(CSVresults, exist_ok=True)
os.makedirs("graphs", exist_ok=True)

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

# cleaned dataset 
cleaned_data = pd.read_csv('CSVs/cleaned_train_data.csv')

# columns dropped during training
drop_cols = ['PATIENT', 'county_name', 'diabetes', 'heart_disease', 'stroke',
             'hypertension', 'asthma', 'copd', 'lung_cancer', 'BIRTHDATE', 'ZIP']

# prepare feature matrix like training
X_full = pd.get_dummies(cleaned_data.drop(columns=drop_cols), drop_first=False)

# file name to target column
def target_from_file(name):
    lower = name.lower()
    if 'diabetes' in lower: return 'diabetes'
    if 'heart_disease' in lower: return 'heart_disease'
    if 'stroke' in lower: return 'stroke'
    if 'hypertension' in lower: return 'hypertension'
    if 'asthma' in lower: return 'asthma'
    if 'copd' in lower: return 'copd'
    if 'lung_cancer' in lower: return 'lung_cancer'
    return ''  

for model_file in os.listdir(models):
    if not model_file.endswith('.pkl'):
        continue

    model_path = os.path.join(models, model_file)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    if not hasattr(model, 'feature_names_in_'):
        print(f"{model_file} has no feature names in")
        continue

    # align x to models training columns
    expected = model.feature_names_in_
    X = X_full.reindex(columns=expected, fill_value=0).copy()

    # choose y based on filename
    target_col = target_from_file(model_file)
    if not target_col or target_col not in cleaned_data.columns:
        print(f"Could not get target for {model_file}")
        continue
    y = cleaned_data[target_col].values

    # scores for ROC
    if hasattr(model, 'predict_proba'):
        y_score = model.predict_proba(X)[:, 1]
    elif hasattr(model, 'decision_function'):
        y_score = model.decision_function(X)
    else:
        y_score = model.predict(X)

    fpr, tpr, thr = roc_curve(y, y_score)
    roc_auc = auc(fpr, tpr)


    # plot ROC curve
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, linewidth=2, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle='--', linewidth=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(model_file.replace('.pkl', '').replace('_', ' ').title() + ' ROC Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()

    # save ROC curve
    roc_img_path = os.path.join(graphresults, model_file.replace('.pkl', '_roc.png'))
    plt.savefig(roc_img_path)
    plt.show()

    print(f"Saved {roc_img_path}")

# open results
results = pd.read_csv("results/results.csv")

# the models to plot
model_types = ["Logistic Regression", "Random Forest", "XGBoost"]

# the metrics to plot
metrics = ["Accuracy", "Recall", "Precision", "F1 Score"]

for model in model_types:
    # flter for just this model type
    df_model = results[results["Model"] == model]

    # ensure order of diseases matches your preference
    diseases = list(df_model["Disease"])
    
    # prepare data for grouped bars
    x = np.arange(len(diseases))  
    width = 0.2  
    offsets = np.linspace(-1.5, 1.5, len(metrics)) * width

    # plot the graphs 
    plt.figure(figsize=(12, 6))
    for i, metric in enumerate(metrics):
        plt.bar(x + offsets[i], df_model[metric], width, label=metric)
    plt.xticks(x, diseases, rotation=45, ha="right")
    plt.ylim(0, 1) 
    plt.ylabel("Score")
    plt.title(f"{model} Performance by Disease")
    plt.legend()
    plt.tight_layout()

    # save the graphs
    filename = f"results/graphs/{model.replace(' ', '_').lower()}_metrics.png"
    plt.savefig(filename, dpi=300)
    plt.show()

    print(f"Saved graph for {model} to {filename}")

   
