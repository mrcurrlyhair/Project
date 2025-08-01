import pandas as pd
import numpy as np

# Seed 28, 10000 Patients, Massachusetts 
np.random.seed(28)

# load the CSV files
observations = pd.read_csv("CSVs/observations.csv")
patients = pd.read_csv("CSVs/patients.csv")
conditions = pd.read_csv("CSVs/conditions.csv")

# filter only the patient health data needed
diseases_cause = [
    "Body Height", "Body Weight", "Systolic Blood Pressure", "Diastolic Blood Pressure",
    "Tobacco smoking status", "Cholesterol [Mass/volume] in Serum or Plasma",
    "Body Mass Index", "Respiratory rate", "Heart rate"
]
observations = observations[observations["DESCRIPTION"].isin(diseases_cause)]

# rename cholesterol column to total colesterol
observations["DESCRIPTION"] = observations["DESCRIPTION"].replace({
    "Cholesterol [Mass/volume] in Serum or Plasma": "Total Cholesterol"
})

# get the latest records for each patients health data
observations["DATE"] = pd.to_datetime(observations["DATE"])
observations = observations.sort_values("DATE", ascending=False)
observations = observations.drop_duplicates(subset=["PATIENT", "DESCRIPTION"], keep="first")

# makes each patients health data have their own column 
observations = observations.pivot(index="PATIENT", columns="DESCRIPTION", values="VALUE").reset_index()

# patient demographics and calculate age
patients_clean = patients[["Id", "BIRTHDATE", "GENDER", "ZIP"]].copy()
patients_clean.rename(columns={"Id": "PATIENT"}, inplace=True)
patients_clean["BIRTHDATE"] = pd.to_datetime(patients_clean["BIRTHDATE"])
patients_clean["AGE"] = (pd.Timestamp("today") - patients_clean["BIRTHDATE"]).dt.days // 365

# unknown zips use previous zips (postcodes) this is for specifically patietns with 00000 as their zipcode
patients_clean["ZIP"] = patients_clean["ZIP"].replace(0, pd.NA)
patients_clean["ZIP"] = patients_clean["ZIP"].fillna(method="ffill")

# merge patient data with their observations data
merged = pd.merge(patients_clean, observations, on="PATIENT", how="left")

# calculate BMI using height in cm and weight in kg
merged["Body Height"] = pd.to_numeric(merged["Body Height"], errors="coerce")
merged["Body Weight"] = pd.to_numeric(merged["Body Weight"], errors="coerce")
merged["BMI"] = round(merged["Body Weight"] / (merged["Body Height"] / 100) ** 2, 1)


# map tobacco smoking status into simpler categories
smoking = {
    "Smokes tobacco daily (finding)": "Current",
    "Ex-smoker (finding)": "Former",
    "Never smoked tobacco (finding)": "Never"
}

merged["smoking_status"] = merged["Tobacco smoking status"].map(smoking).fillna("Unknown")
merged.drop(columns=["Tobacco smoking status"], inplace=True)


# different terms for the same diseases
diseases_terms = {
    "heart_disease": ["myocardial infarction", "coronary artery disease", "chronic congestive heart failure"],
    "stroke": ["stroke", "ischemic stroke", "cerebrovascular accident"],
    "hypertension": ["hypertension"],
    "copd": ["chronic obstructive pulmonary disease", "chronic obstructive bronchitis"],
    "asthma": ["asthma"],
    "lung_cancer": ["lung cancer"],
    "diabetes": ["diabetes", "type 2", "diabetes mellitus type 2", "disorder of kidney due to diabetes mellitus"]
}

# add empty columns for each disease
for col in diseases_terms:
    merged[col] = 0

# check each condition and update the label if it matches (1 for true or 0 for false)
for i, row in conditions.iterrows():
    pid = row["PATIENT"]
    desc = str(row["DESCRIPTION"]).lower()
    for label, words in diseases_terms.items():
        for word in words:
            if word in desc:
                merged.loc[merged["PATIENT"] == pid, label] = 1
                break


# alcohol use - None, Light, Moderate, Heavy
def alcohol_use(row):
    if row["AGE"] >= 65:
        probs = [0.40, 0.45, 0.11, 0.04]
    elif row["AGE"] <= 34:
        probs = [0.30, 0.50, 0.16, 0.04]
    else:
        probs = [0.34, 0.46, 0.15, 0.05]
    return np.random.choice(["Sober", "Light", "Moderate", "Heavy"], p=probs)

# physical activity 
def physical_activity(row):
    if row["AGE"] >= 65:
        return np.random.choice(["Sedentary", "Moderate", "Active"], p=[0.25, 0.60, 0.15])
    else:
        return np.random.choice(["Sedentary", "Moderate", "Active"], p=[0.25, 0.45, 0.30])

# diet quality 
def diet_quality(row):
    if row["diabetes"] == 1:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.50, 0.35, 0.15])
    elif row["BMI"] > 30:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.45, 0.35, 0.20])
    else:
        return np.random.choice(["Poor", "Average", "Healthy"], p=[0.25, 0.40, 0.35])

# sleep hours
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

# change invalid data to nan to be then added with mean
merged["Total Cholesterol"] = pd.to_numeric(merged["Total Cholesterol"], errors="coerce")

# add missing total cholesterol with mean
merged["Total Cholesterol"] = merged["Total Cholesterol"].fillna(round(merged["Total Cholesterol"].mean(), 1))


# load uszips csv 
zipcode = pd.read_csv("CSVs/uszips.csv", dtype={"zip": str}, low_memory=False)

# load only masachusetts zips
zipcounty = zipcode[zipcode["state_id"] == "MA"][["zip", "county_name"]]

# define radon level 5 = high / 3 = moderate / 1 = low
radon = {
    "Worcester": 5,
    "Middlesex": 5,
    "Essex": 5,
    "Norfolk": 3,
    "Plymouth": 3,
    "Barnstable": 3,
    "Bristol": 3,
    "Hampden": 3,
    "Hampshire": 3,
    "Franklin": 3,
    "Berkshire": 3,
    "Suffolk": 1,
    "Dukes": 3,
    "Nantucket": 3
}

# assign radon levels based on county
zipcounty["radon_level"] = zipcounty["county_name"].map(radon)

# Missing zip code
missingzips = [
    {"zip": "01866", "county_name": "Middlesex", "radon_level": 5},
    {"zip": "01086", "county_name": "Hampden",   "radon_level": 3},
    {"zip": "01199", "county_name": "Hampden",   "radon_level": 3},
    {"zip": "02861", "county_name": "Bristol",   "radon_level": 3},
    {"zip": "02554", "county_name": "Dukes",     "radon_level": 3},
    {"zip": "01059", "county_name": "Hampshire", "radon_level": 3},
    {"zip": "02768", "county_name": "Plymouth",  "radon_level": 3},
    {"zip": "02060", "county_name": "Norfolk",   "radon_level": 3},
    {"zip": "02358", "county_name": "Plymouth",  "radon_level": 3},
    {"zip": "02574", "county_name": "Barnstable","radon_level": 3},
    {"zip": "02543", "county_name": "Barnstable","radon_level": 3},
    {"zip": "02568", "county_name": "Dukes",     "radon_level": 3},
    {"zip": "02669", "county_name": "Barnstable","radon_level": 3},
    {"zip": "02651", "county_name": "Barnstable","radon_level": 3},
    {"zip": "02051", "county_name": "Plymouth",  "radon_level": 3}
]

# add missing zips, this method is the only one that consistently worked after some odd issues. :)
missingzip = pd.DataFrame(missingzips)
missingzip["zip"] = missingzip["zip"].astype(str).str.zfill(5)

# combine into zipcounty
zipcounty = pd.concat([zipcounty, missingzip], ignore_index=True)

# prepare zip codes, need to be 5 digits long 
merged["ZIP"] = merged["ZIP"].astype(str).str.zfill(5)

# code to print missing zips 
# unmatched_zips = merged[merged["county_name"].isna()]["ZIP"].unique()
# print("Unmatched ZIP codes:", unmatched_zips)

# merge  
merged = merged.merge(zipcounty, left_on="ZIP", right_on="zip", how="left")

# delete extra zip column
merged.drop(columns=["zip"], inplace=True)

# Prepare pollution data
pollution = pd.read_csv("CSVs/pollution_levels.csv")
pollution["county_name"] = pollution["County"].str.replace(" County", "", regex=False)
pollution.rename(columns={"Micrograms per cubic meter (PM2.5)": "pollution"}, inplace=True)
pollution = pollution[["county_name", "pollution"]]

# merge pollution data into merged dataset using county_name
merged = merged.merge(pollution, on="county_name", how="left")

# save the cleaned dataset
merged.to_csv("CSVs/cleaned_train_data.csv", index=False)
print("Cleaned train data saved ")
