# Streamlit UI
st.set_page_config(page_title="Nutrition Paradox", layout="wide")
st.title("\u2696\ufe0f Nutrition Paradox Dashboard")

# Tabs for categorization
tabs = st.tabs([
    "Obesity Queries", "Malnutrition Queries", "Combined Queries"
])

# --- Obesity Queries --- #
with tabs[0]:
    st.header("\U0001F9CB Obesity Analysis")
    queries = [
        ("Top 5 regions with highest avg obesity levels in 2022", """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            WHERE Year = 2022
            GROUP BY Region
            ORDER BY Avg_Obesity DESC
            LIMIT 5;
        """),

        ("Top 5 countries with highest obesity estimates", """
            SELECT Country, MAX(Mean_Estimate) AS Max_Obesity
            FROM obesity
            GROUP BY Country
            ORDER BY Max_Obesity DESC
            LIMIT 5;
        """),

        ("Obesity trend in India over the years", """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            WHERE Country = 'India'
            GROUP BY Year
            ORDER BY Year;
        """),

        ("Average obesity by gender", """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY Gender;
        """),

        ("Country count by obesity level category and age group", """
            SELECT Obesity_Level, Age_Group, COUNT(DISTINCT Country) AS Country_Count
            FROM obesity
            GROUP BY Obesity_Level, Age_Group;
        """),

        ("Top 5 most and least consistent countries by CI_Width", """
            (SELECT Country, AVG(CI_Width) AS Avg_CI FROM obesity GROUP BY Country ORDER BY Avg_CI DESC LIMIT 5)
            UNION
            (SELECT Country, AVG(CI_Width) AS Avg_CI FROM obesity GROUP BY Country ORDER BY Avg_CI ASC LIMIT 5);
        """),

        ("Average obesity by age group", """
            SELECT Age_Group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY Age_Group;
        """),

        ("Top 10 countries with consistent low obesity", """
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM obesity
            GROUP BY Country
            HAVING Avg_Obesity < 25 AND Avg_CI < 5
            ORDER BY Avg_Obesity ASC
            LIMIT 10;
        """),

        ("Countries where female obesity exceeds male by large margin", """
            SELECT o1.Country, o1.Year, o1.Mean_Estimate AS Female_Obesity, o2.Mean_Estimate AS Male_Obesity
            FROM obesity o1
            JOIN obesity o2 ON o1.Country = o2.Country AND o1.Year = o2.Year
            WHERE o1.Gender = 'Female' AND o2.Gender = 'Male' AND o1.Mean_Estimate - o2.Mean_Estimate > 5;
        """),

        ("Global average obesity percentage per year", """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Global_Avg_Obesity
            FROM obesity
            GROUP BY Year
            ORDER BY Year;
        """),
    ]

    for title, q in queries:
        st.subheader(title)
        df = run_query(q)
        st.dataframe(df)
        if "Year" in df.columns and "Avg" in ''.join(df.columns):
            fig = px.line(df, x='Year', y=df.columns[-1], title=title)
            st.plotly_chart(fig, use_container_width=True)
with tabs[1]:
    st.header("\U0001F9C2 Malnutrition Analysis")
    queries = [
        ("Avg. malnutrition by age group", """
            SELECT Age_Group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Age_Group;
        """),

        ("Top 5 countries with highest malnutrition", """
            SELECT Country, MAX(Mean_Estimate) AS Max_Malnutrition
            FROM malnutrition
            GROUP BY Country
            ORDER BY Max_Malnutrition DESC
            LIMIT 5;
        """),

        ("Malnutrition trend in African region", """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Africa_Avg
            FROM malnutrition
            WHERE Region = 'Africa'
            GROUP BY Year
            ORDER BY Year;
        """),

        ("Gender-based average malnutrition", """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Gender;
        """),

        ("Malnutrition level-wise CI_Width by age group", """
            SELECT Malnutrition_Level, Age_Group, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM malnutrition
            GROUP BY Malnutrition_Level, Age_Group;
        """),

        ("Yearly malnutrition change in India, Nigeria, Brazil", """
            SELECT Country, Year, ROUND(AVG(Mean_Estimate), 2) AS Avg
            FROM malnutrition
            WHERE Country IN ('India', 'Nigeria', 'Brazil')
            GROUP BY Country, Year
            ORDER BY Country, Year;
        """),

        ("Regions with lowest malnutrition averages", """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Region
            ORDER BY Avg_Malnutrition ASC
            LIMIT 5;
        """),

        ("Countries with increasing malnutrition", """
            SELECT Country, MIN(Mean_Estimate) AS Min_Est, MAX(Mean_Estimate) AS Max_Est
            FROM malnutrition
            GROUP BY Country
            HAVING Max_Est - Min_Est > 5;
        """),

        ("Min/Max malnutrition levels year-wise", """
            SELECT Year, MIN(Mean_Estimate) AS Min_Level, MAX(Mean_Estimate) AS Max_Level
            FROM malnutrition
            GROUP BY Year
            ORDER BY Year;
        """),

        ("High CI_Width flags", """
            SELECT Country, Year, CI_Width
            FROM malnutrition
            WHERE CI_Width > 5;
        """),
    ]
    for title, q in queries:
        st.subheader(title)
        df = run_query(q)
        st.dataframe(df)
        if "Year" in df.columns and ("Avg" in ''.join(df.columns) or "Africa_Avg" in df.columns):
            fig = px.line(df, x='Year', y=df.columns[-1], title=title)
            st.plotly_chart(fig, use_container_width=True)

# --- Combined Queries --- #
with tabs[2]:
    st.header("\U0001F517 Combined Nutrition Analysis")
    queries = [
        ("Obesity vs malnutrition comparison for selected countries", """
            SELECT o.Country, o.Year, o.Mean_Estimate AS Obesity, m.Mean_Estimate AS Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
            WHERE o.Country IN ('India', 'USA', 'Brazil', 'Nigeria', 'China');
        """),

        ("Gender-based disparity in both", """
            SELECT o.Gender, ROUND(AVG(o.Mean_Estimate), 2) AS Avg_Obesity, ROUND(AVG(m.Mean_Estimate), 2) AS Avg_Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year AND o.Gender = m.Gender
            GROUP BY o.Gender;
        """),

        ("Region-wise avg estimates side-by-side (Africa and Americas)", """
            SELECT o.Region, ROUND(AVG(o.Mean_Estimate), 2) AS Obesity_Avg, ROUND(AVG(m.Mean_Estimate), 2) AS Malnutrition_Avg
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
            WHERE o.Region IN ('Africa', 'Americas Region')
            GROUP BY o.Region;
        """),

        ("Countries with obesity up & malnutrition down", """
            SELECT o.Country
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
            GROUP BY o.Country
            HAVING MAX(o.Mean_Estimate) - MIN(o.Mean_Estimate) > 5
               AND MIN(m.Mean_Estimate) - MAX(m.Mean_Estimate) > -5;
        """),

        ("Age-wise trend analysis", """
            SELECT o.Year, o.Age_Group, ROUND(AVG(o.Mean_Estimate), 2) AS Obesity, ROUND(AVG(m.Mean_Estimate), 2) AS Malnutrition
            FROM obesity o
            JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year AND o.Age_Group = m.Age_Group
            GROUP BY o.Year, o.Age_Group
            ORDER BY o.Year;
        """),
    ]
    for title, q in queries:
        st.subheader(title)
        df = run_query(q)
        st.dataframe(df)
        if "Year" in df.columns and ("Obesity" in df.columns or "Malnutrition" in df.columns):
            fig = px.line(df, x='Year', y=df.columns[-1], title=title, color=df.columns[1] if df.shape[1] > 2 else None)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Built for Nutrition Paradox Capstone Project")
