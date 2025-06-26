import pandas as pd
import numpy as np

# Seed 28, 10000 patients, Massachusetts 

# Load the CSV files
observations = pd.read_csv("CSVs/observations.csv")
patients = pd.read_csv("CSVs/patients.csv")
conditions = pd.read_csv("CSVs/conditions.csv")

# Filter only the patient health data needed
diseases = [
    "Body Height", "Body Weight", "Systolic Blood Pressure", "Diastolic Blood Pressure",
    "Tobacco smoking status", "Cholesterol", "HDL Cholesterol", "LDL Cholesterol",
    "Body Mass Index", "Respiratory rate", "Heart rate"
]
observations = observations[observations["DESCRIPTION"].isin(diseases)]

# Get the latest records for each patients health data
observations["DATE"] = pd.to_datetime(observations["DATE"])
observations = observations.sort_values("DATE", ascending=False)
observations = observations.drop_duplicates(subset=["PATIENT", "DESCRIPTION"], keep="first")

# Makes patient health data have their own column 
observations = observations.pivot(index="PATIENT", columns="DESCRIPTION", values="VALUE").reset_index()

# Patient demographics and calculate age
patients_clean = patients[["Id", "BIRTHDATE", "GENDER", "ZIP"]].copy()
patients_clean.rename(columns={"Id": "PATIENT"}, inplace=True)
patients_clean["BIRTHDATE"] = pd.to_datetime(patients_clean["BIRTHDATE"])
patients_clean["AGE"] = (pd.Timestamp("today") - patients_clean["BIRTHDATE"]).dt.days // 365

# Unknown zips use preious zips (postcodes)
patients_clean["ZIP"] = patients_clean["ZIP"].replace(0, pd.NA)
patients_clean["ZIP"] = patients_clean["ZIP"].fillna(method="ffill")

# Merge patient data with their observations data
merged = pd.merge(patients_clean, observations, on="PATIENT", how="left")

# Calculate BMI using height in cm and weight in kg
merged["Body Height"] = pd.to_numeric(merged["Body Height"], errors="coerce")
merged["Body Weight"] = pd.to_numeric(merged["Body Weight"], errors="coerce")
merged["BMI"] = round(merged["Body Weight"] / (merged["Body Height"] / 100) ** 2, 1)


# Map tobacco smoking status into simpler categories
smoking = {
    "Smokes tobacco daily (finding)": "Current",
    "Ex-smoker (finding)": "Former",
    "Never smoked tobacco (finding)": "Never"
}

merged["smoking_status"] = merged["Tobacco smoking status"].map(smoking).fillna("Unknown")
merged.drop(columns=["Tobacco smoking status"], inplace=True)


# Different terms for the same diseases
diseases_terms = {
    "heart_disease": ["myocardial infarction", "coronary artery disease", "chronic congestive heart failure"],
    "stroke": ["stroke", "ischemic stroke", "cerebrovascular accident"],
    "hypertension": ["hypertension"],
    "copd": ["chronic obstructive pulmonary disease", "chronic obstructive bronchitis"],
    "asthma": ["asthma"],
    "lung_cancer": ["lung cancer"],
    "diabetes": ["diabetes", "type 2", "diabetes mellitus type 2", "disorder of kidney due to diabetes mellitus"]
}

# Add empty columns for each disease
for col in diseases_terms:
    merged[col] = 0

# Check each condition and update the label if it matches (1 for true or 0 for false)
for i, row in conditions.iterrows():
    pid = row["PATIENT"]
    desc = str(row["DESCRIPTION"]).lower()
    for label, words in diseases_terms.items():
        for word in words:
            if word in desc:
                merged.loc[merged["PATIENT"] == pid, label] = 1
                break


# Alcohol use - None, Light, Moderate, Heavy
def alcohol_use(row):
    if row["AGE"] >= 65:
        probs = [0.40, 0.45, 0.11, 0.04]
    elif row["AGE"] <= 34:
        probs = [0.30, 0.50, 0.16, 0.04]
    else:
        probs = [0.34, 0.46, 0.15, 0.05]
    return np.random.choice(["None", "Light", "Moderate", "Heavy"], p=probs)

# Physical activity 
def physical_activity(row):
    if row["AGE"] >= 65:
        return np.random.choice(["Sedentary", "Moderate", "Active"], p=[0.25, 0.60, 0.15])
    else:
        return np.random.choice(["Sedentary", "Moderate", "Active"], p=[0.25, 0.45, 0.30])

# Diet quality 
def diet_quality(row):
    if row["diabetes"] == 1:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.50, 0.35, 0.15])
    elif row["BMI"] > 30:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.45, 0.35, 0.20])
    else:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.25, 0.40, 0.35])

# Sleep hours
def sleep_hours(row):
    if row["AGE"] >= 65:
        return round(np.random.normal(6.3, 1), 1)
    elif row["AGE"] <= 25:
        return round(np.random.normal(7.5, 1), 1)
    elif row["smoking_status"] == "Current":
        return round(np.random.normal(6.0, 1), 1)
    else:
        return round(np.random.normal(7.0, 1), 1)

# add snythetic data for each patient 
merged["alcohol_use"] = merged.apply(alcohol_use, axis=1)
merged["physical_activity"] = merged.apply(physical_activity, axis=1)
merged["diet_quality"] = merged.apply(diet_quality, axis=1)
merged["sleep_hours"] = merged.apply(sleep_hours, axis=1)

# Save the cleaned dataset
merged.to_csv("CSVs/cleaned_data.csv", index=False)
print("Cleaned dataset saved ")
