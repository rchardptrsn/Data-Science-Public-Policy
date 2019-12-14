import streamlit as st
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import psycopg2 as pg


st.image(image='censusimg.jpg',caption='https://pixabay.com/illustrations/magnifying-glass-human-head-faces-1607208/')

st.title('Census Data Exploration')
st.header('Explore socially important metrics using Seaborn and Streamlit')
st.write('This exploration uses data from American Community Survey 5-year data released in 2017.')
st.write('More information about the ACS 5-year survey: https://www.census.gov/data/developers/data-sets/acs-5year.html')
st.write("The data was collected using Julien Leider's CensusData pip package, which can be found at https://pypi.org/project/CensusData/ or installed with")
st.code('pip install CensusData')

st.header('County Level Summaries')
st.write('This analysis will use data aggregated on the county level for the variables: Gini Index (income inequality index), Vacant Housing, Percent Unemployed and Median Family Income.')

# SQL database query function
def censusquery(sqlquery):


    import psycopg2
    import pandas as pd
    conn_string = "host='104.248.112.101' dbname='censusdata' user='richard' password='Zx45hud1zx45hud'"
    print("Connecting to database.")
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sqlquery)
    tmp = cursor.fetchall()
    col_names = []
    for elt in cursor.description:
        col_names.append(elt[0])
    df = pd.DataFrame(tmp,columns=col_names)
    print("Connection Successful. Query complete.")
    return df


# Write the query
sqlquery = 'SELECT gini_index,vacant_housing,percent_unemployed,median_family_income from census;'

# Call the function to execute the query.
df = censusquery(sqlquery)
df.columns = ['Gini Index', 'Vacant Housing', 'Percent Unemployed', 'Median Family Income']

# Dataframe for median family income Statistics
st.subheader('Descriptive Statistics for Median Family Income')
st.write(df['Median Family Income'].describe().round())

# Histogram for median family income
st.subheader('Seaborn distplot of Median Family Income')
plt.figure()
plt.title('County Level Income Distribution')
sns.set_style('darkgrid')
sns.distplot(df['Median Family Income'])
st.pyplot()

# Create a new column based on median family income called 'Income Quartile'.
df['Income Quartile'] = pd.qcut(df['Median Family Income'],q=4,labels=False,precision=0,duplicates='raise')
# Zero-based, raise by 1
df['Income Quartile'] = df['Income Quartile'] + 1

# Scatterplot for median family income by quartile
st.subheader('Seaborn scatterplot of Median Family Income by Percent Unemployed')
plt.figure()
sns.set_style('darkgrid')
plt.title('Median Family Income versus Unemployment')
sns.scatterplot(x='Median Family Income',y='Percent Unemployed',data=df,hue='Income Quartile',palette="Dark2")
st.pyplot()

# Checkbox for lmplot analysis
st.subheader('Please select an X and Y value for analysis' )
x_axis = st.selectbox(
    'Pick an X-axis value:',
     ['Gini Index', 'Vacant Housing', 'Percent Unemployed', 'Median Family Income'])
y_axis = st.selectbox(
    'Pick a Y-axis value:',
     ['Percent Unemployed','Gini Index', 'Vacant Housing','Median Family Income'])
sns.set()
plt.figure()
sns.set_style('darkgrid')
plt.title('Seaborn lmplot analysis by Income Quartile')
sns.set_context("paper", font_scale=1.3) 
sns.lmplot(x=x_axis, y=y_axis, data=df, hue='Income Quartile',col='Income Quartile',col_wrap=2)
st.pyplot()





