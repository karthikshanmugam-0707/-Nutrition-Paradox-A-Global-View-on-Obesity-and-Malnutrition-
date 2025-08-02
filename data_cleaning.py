# Step 1: Rename columns for consistency
df_obesity = df_obesity.rename(columns={
    'TimeDim': 'Year',
    'Dim1': 'Gender',
    'NumericValue': 'Mean_Estimate',
    'Low': 'LowerBound',
    'High': 'UpperBound',
    'ParentLocation': 'Region',
    'SpatialDim': 'Country'
})
# Step 2: Standardize Gender values
df_obesity['Gender'] = df_obesity['Gender'].replace({
    'SEX_BTSX': 'Both',
    'SEX_MLE': 'Male',
    'SEX_FMLE': 'Female'
})
# Step 3: Create CI_Width column
df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']

# Step 4: Create obesity_level column
def get_obesity_level(value):
    if value >= 30:
        return 'High'
    elif 25 <= value < 30:
        return 'Moderate'
    else:
        return 'Low'

df_obesity['obesity_level'] = df_obesity['Mean_Estimate'].apply(get_obesity_level)

# Step 5: Using pycounty to exctracting country name for the 3 letter alpha codes data. 
import pycountry
def convert_country(code):
    if not isinstance(code, str):
        return None
    try:
        country = pycountry.countries.get(alpha_3=code.upper())
        return country.name if country else None
    except Exception:
        return None

df_obesity['Country'] = df_obesity['Country'].apply(convert_country)
# Step 6: Replace any None values in Country with special mappings
special_cases = {
    'GLOBAL': 'Global',
    'WB_LMI': 'Low & Middle Income',
    'WB_HI': 'High Income',
    'WB_LI': 'Low Income',
    'EMR': 'Eastern Mediterranean Region',
    'EUR': 'Europe',
    'AFR': 'Africa',
    'SEAR': 'South-East Asia Region',
    'WPR': 'Western Pacific Region',
    'AMR': 'Americas Region',
    'WB_UMI': 'Upper Middle Income'
}

df_obesity['Country'] = df_obesity['Country'].fillna(df_obesity['Country'].map(special_cases))

# Step 7: Filter only years between 2012 to 2022
df_obesity = df_obesity[(df_obesity['Year'] >= 2012) & (df_obesity['Year'] <= 2022)]

# Repeat the same steps for malnutrition datas also expect step 4: for mal-nutrition the step 4 should be changed to

def get_malnutrition_level(value):
    if value >= 20:
        return 'High'
    elif 10 <= value < 20:
        return 'Moderate'
    else:
        return 'Low'

df_malnutrient['malnutrition_level'] = df_malnutrient['Mean_Estimate'].apply(get_malnutrition_level)
# Step 5: Create CI_Width column
df_malnutrient['CI_Width'] = df_malnutrient['UpperBound'] - df_malnutrient['LowerBound']
