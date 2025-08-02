import requests
import pandas as pd

# WHO API base
base_url = "https://ghoapi.azureedge.net/api/"

# Dataset codes
dataset_codes = {
    "adult_obesity": "NCD_BMI_30C",
    "child_obesity": "NCD_BMI_PLUS2C",
    "adult_malnutrition": "NCD_BMI_18C",
    "child_malnutrition": "NCD_BMI_MINUS2C"
}

# Function to load and convert API response to DataFrame
def load_dataset(code):
    url = base_url + code
    response = requests.get(url)
    data = response.json()['value']
    return pd.DataFrame(data)

# Load datasets
df_adult_obesity = load_dataset(dataset_codes["adult_obesity"])
df_child_obesity = load_dataset(dataset_codes["child_obesity"])
df_adult_malnutrition = load_dataset(dataset_codes["adult_malnutrition"])
df_child_malnutrition = load_dataset(dataset_codes["child_malnutrition"])

# Add age group labels
df_adult_obesity["age_group"] = "Adult"
df_child_obesity["age_group"] = "Child/Adolescent"
df_adult_malnutrition["age_group"] = "Adult"
df_child_malnutrition["age_group"] = "Child/Adolescent"

# Merge into 2 master datasets
df_obesity = pd.concat([df_adult_obesity, df_child_obesity], ignore_index=True)
df_malnutrition = pd.concat([df_adult_malnutrition, df_child_malnutrition], ignore_index=True)

# Filter for years 2012 to 2022
df_obesity = df_obesity[df_obesity['TimeDim'].between(2012, 2022)]
df_malnutrition = df_malnutrition[df_malnutrition['TimeDim'].between(2012, 2022)]

# Save the datasets as CSV files
df_obesity.to_csv("obesity_data.csv", index=False)
df_malnutrition.to_csv("malnutrition_data.csv", index=False)

print("✅ CSV files saved: 'obesity_data.csv' and 'malnutrition_data.csv'")
