import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

def create_riders_per_seasonhour(df):
    results = (
    df.groupby(['season', 'hr'])['cnt']
    .sum()  # Calculate the sum of 'cnt' for each season and hour
    .groupby(level=0)  # Group by 'season'
    .nlargest(5)  # Select the top 5 highest 'cnt' values for each season
    .droplevel(level=0)
    )
    return results

def create_riders_per_holiday(df):
    results = (
    df[df['holiday'] == 1]  # Filter for holidays
    [['dteday', 'season', 'weathersit', 'weekday', 'cnt', ]]  # Select the specified columns
    .sort_values(by='cnt', ascending=False)  # Sort by 'cnt' in descending order
    .nlargest(n=5, columns='cnt')
    )
    return results

def create_ridership_shares(df):
    pass

def create_riders_per_season(df):
    results = df.groupby(by='season')['cnt'].sum(True)
    return results

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


#load data

bike_sharing_day = pd.read_csv("day.csv")
bike_sharing_hour = pd.read_csv("hour.csv")


#dataframe prep
ridership_per_seasonhour = create_riders_per_seasonhour(bike_sharing_hour)
riders_per_holiday = create_riders_per_holiday(bike_sharing_day)
riders_per_season = create_riders_per_season(bike_sharing_day)

#visualization section

st.set_page_config(page_title='D.C 2011-2012 Bike Sharing Review')
st.header('D.C. 2011-2012 Bike Sharing Data Review')

labels = ['Registered Rider', 'Casual Rider']
rider_counts = [
    bike_sharing_day['registered'].sum(numeric_only=True),
    bike_sharing_day['casual'].sum(numeric_only=True),
    bike_sharing_day['cnt'].sum(numeric_only=True)
]

st.write('''### Ridership shares''')
st.write(f'Total riderships: {rider_counts[2]}')
fig1, ax1 = plt.subplots()
ax1.set_title('Ridership shares 2011-2012', loc='center')
ax1.pie(rider_counts[0:2], labels=labels, autopct=make_autopct(rider_counts), startangle=90, textprops={'fontsize': 8})
ax1.axis('equal')
st.pyplot(fig1)

col1, col2 = st.columns(2)

with col1:
    st.write('''### Bagaimana kah 5 besar pengendara rental pada tiap *holiday*?''')
    
    riders_per_holiday.pivot_table(values='cnt', index='dteday').plot(kind='bar')
    #result.unstack().plot(kind='bar')
    plt.title("5 Highest Ridership per holiday")
    plt.xlabel("Holiday date")
    plt.ylabel("Ridership Count (cnt)")
    st.pyplot(plt.show())
    
    exp1 = st.expander('Legends')
    exp1.write('''#### Holiday for each date:
    2011-07-04: Fourth of July Independence Day
    2012-04-06: D.C. Emancipation Day
    2012-05-28: Memorial Day
    2012-07-04: Fourth of July Independence Day
    2012-11-12: Veteran Day''')
    
with col2:
    st.write('''### Bagaimana kah 5 besar *peak hour* rental pada setiap musim?''')
    ridership_per_seasonhour.unstack().plot(kind='bar')
    plt.title("5 Highest Ridership Hours for Each Season")
    plt.xlabel("Season")
    plt.ylabel("Ridership Count (cnt)")
    st.pyplot(plt.show())
    
    exp1 = st.expander('Legends')
    exp1.write('''#### Season number meaning:
    1 = Winter
    2 = Spring
    3 = Summer
    4 = Fall''')
    
st.caption('Copyright © Aria Abdurrahman Airlangga')