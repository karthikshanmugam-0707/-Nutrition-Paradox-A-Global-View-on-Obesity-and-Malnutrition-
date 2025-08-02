pip install mysql-connector-python
import mysql.connector
# Connect to MySQL server (no database yet)
conn = mysql.connector.connect(
    host="****",        # or your MySQL server IP
    user="****",
    password="****",
    port=4000,
    database="nutrition_db"
)
cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS nutrition_db")
print("✅ Database created!")

# Create table Obesity
cursor.execute("""
CREATE TABLE IF NOT EXISTS obesity (
    Year INT,
    Gender VARCHAR(10),
    Mean_Estimate FLOAT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    Age_Group VARCHAR(20),
    Country VARCHAR(100),
    Region VARCHAR(100),
    CI_Width FLOAT,
    Obesity_Level VARCHAR(15)
)
""")
print("✅ Obesity table created!")

# Data insertion into Obesity table
data_to_insert = []
for _, row in df_obesity.iterrows():
  data_to_insert.append((
        int(row['Year']),
        row['Gender'],
        float(row['Mean_Estimate']),
        float(row['LowerBound']),
        float(row['UpperBound']),
        row['age_group'],
        row['Country'],
        row['Region'],
        float(row['CI_Width']),
        row['obesity_level']
    ))
query = """
    INSERT INTO obesity (
        Year, Gender, Mean_Estimate, LowerBound, UpperBound,
        Age_Group, Country, Region, CI_Width, Obesity_Level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(query, data_to_insert)
conn.commit()
print("✅ Obesity data inserted successfully!")

# Malnutrition table Creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS malnutrition (
    Year INT,
    Gender VARCHAR(10),
    Mean_Estimate FLOAT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    Age_Group VARCHAR(20),
    Country VARCHAR(100),
    Region VARCHAR(100),
    CI_Width FLOAT,
    Malnutrition_Level VARCHAR(15)
)
""")
print("✅ Malnutrition table created!")

# Data insertion into Malnutrition table
data_to_insert_malnutrition = []
for _, row in df_malnutrient.iterrows():
    data_to_insert_malnutrition.append((
        int(row['Year']),
        row['Gender'],
        float(row['Mean_Estimate']),
        float(row['LowerBound']),
        float(row['UpperBound']),
        row['age_group'],
        row['Country'],
        row['Region'],
        float(row['CI_Width']),
        row['malnutrition_level']
    ))

query_malnutrition = """
    INSERT INTO malnutrition (
        Year, Gender, Mean_Estimate, LowerBound, UpperBound,
        Age_Group, Country, Region, CI_Width, Malnutrition_Level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query_malnutrition, data_to_insert_malnutrition)
conn.commit()
print("✅ Malnutrition data inserted successfully!")
