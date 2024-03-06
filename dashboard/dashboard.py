import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Ignore FutureWarnings and UserWarnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


all_df = pd.read_csv("hour.csv")
datetime_columns = ["dteday"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column]).dt.date


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("logo.png")
    
    # Mengambil tanggal
    selected_date = st.date_input(
        label='Tampilkan Grafik Perhari',
        min_value=min_date,
        max_value=max_date,
        value=min_date  # Atau tanggal lainnya yang diinginkan
    )

    month = st.selectbox(
        label="Lihat Statistik Bulanan",
        options=("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    )

    year = st.selectbox(
        label="Pilih tahun",
        options=("2011", "2012")
    )

    

hourly_rent_df = all_df[(all_df["dteday"] == selected_date)]

year_dict = {"2011": 0, "2012":1}

month_dict = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}
month_num = month_dict[month]
year_num = year_dict[year]

def denormalize_temperature(normalized_value):
    t_min = -8
    t_max = 39
    temperature = t_min + normalized_value * (t_max - t_min)
    return temperature

weather_labels = {
    1: 'Cerah',
    2: 'Berawan',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}

seasons_labels = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

st.header('Bike Sharing Dashboard :bike:')



col1, col2 = st.columns(2)
 
with col1:
    temperature = denormalize_temperature(hourly_rent_df['temp'].mean())
    st.metric(label="Temperature", value="{:.1f} °C".format(temperature))
 
with col2:
    weather_num = (hourly_rent_df['weathersit'].mode().iloc[0])
    weather = weather_labels[weather_num]
    st.metric(label="Weather", value=weather)


st.subheader('Hourly Bike Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_rent_df["hr"],
    hourly_rent_df["cnt"],
    marker='o', 
    linewidth=2,
    color="g"
    
)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(hourly_rent_df["hr"])

st.pyplot(fig)

peak_hour_row = hourly_rent_df.loc[hourly_rent_df['cnt'].idxmax()]
peak_hour = peak_hour_row['hr']
st.write("Puncak peminjaman sepeda hari ini terjadi pada jam {} sebanyak {}".format(peak_hour, peak_hour_row['cnt']))






new_df = all_df.copy()
new_df['season'] = new_df['season'].map(seasons_labels)
new_df['weathersit'] = new_df['weathersit'].map(weather_labels)
# st.write(selected_date)


# st.dataframe(data=new_df, width=500, height=150)
by_month_df = new_df[(new_df["mnth"] == month_num) & (new_df["yr"] == year_num)]
by_year_df = new_df[new_df["yr"] == year_num]


average_rent_by_weather = by_month_df.groupby('weathersit')['cnt'].mean().reset_index().sort_values("cnt")
# st.dataframe(data=average_rent_by_weather, width=500, height=150)
averages_rent_by_season = by_year_df.groupby('season')['cnt'].mean().reset_index()
# st.dataframe(data=averages_rent_by_season, width=500, height=150)


st.subheader("Number of Rentals Based on Weather and Season") 
fig, ax = plt.subplots(figsize=(20, 10))
colors_1 = ["#87CEEB", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="weathersit",
    y="cnt",
    data=average_rent_by_weather.sort_values(by="cnt", ascending=False),
    palette=colors_1
)
ax.set_ylabel("Number of Rents", fontsize=30)
ax.set_xlabel(None)
ax.set_title("Bike Rentals by Weather condition in {} {}".format(month, year), loc="center", fontsize=35)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)



fig, ax = plt.subplots(figsize=(20, 10))
colors_2 = ["#D3D3D3", "#D3D3D3", "#87CEEB", "#D3D3D3"]
sns.barplot(
    x="season",
    y="cnt",
    data=averages_rent_by_season,
    palette=colors_2,
    order=['Spring', 'Summer', 'Fall', 'Winter']
)
ax.set_ylabel("Number of Rents", fontsize=30)
ax.set_xlabel(None)
# ax.yaxis.set_label_position("right")
# ax.yaxis.tick_right()
ax.set_title("Bike Rentals by Weather Season in {}".format(year), loc="center", fontsize=35)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)



st.caption('by Muhammad Dzaky Khairy')