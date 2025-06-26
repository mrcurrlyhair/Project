import pandas as pd

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

# Merge patient data with their observations data
merged = pd.merge(patients_clean, observations, on="PATIENT", how="left")

# different terms for the same diseases
diseases_terms = {
    "heart_disease": ["myocardial infarction", "coronary artery disease"],
    "stroke": ["stroke", "ischemic stroke"],
    "hypertension": ["hypertension"],
    "copd": ["chronic obstructive pulmonary disease"],
    "asthma": ["asthma"],
    "lung_cancer": ["lung cancer"],
    "diabetes": ["diabetes", "type 2"]
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

# Save the cleaned dataset
merged.to_csv("CSVs/cleaned_data.csv", index=False)
print("Cleaned dataset saved ")
