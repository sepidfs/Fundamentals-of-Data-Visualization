# -------------------------------------
# 📦 Install & Import Dependencies
# -------------------------------------
import sys, subprocess, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import altair_viewer
import plotly.express as px

# Install required packages
def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["pandas", "altair", "altair_viewer", "matplotlib", "seaborn", "plotly"]:
    install_if_missing(pkg)

# -------------------------------------
# 📂 Paths & Load Data
# -------------------------------------
file_path = r"C:\Users\14163\Desktop\university cu boulder\Fundamentals of Data Visualization\Data\netflix_titles.csv"
out_dir = r"C:\Users\14163\Desktop\university cu boulder\Fundamentals of Data Visualization\Data"
os.makedirs(out_dir, exist_ok=True)

df = pd.read_csv(file_path)
alt.data_transformers.disable_max_rows()

# -------------------------------------
#   Top 10 Genres
# -------------------------------------
genres = df['listed_in'].dropna().str.split(', ')
genres_exploded = genres.explode()
top_genres = genres_exploded.value_counts().head(10)

plt.figure(figsize=(14, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette="Set2")
plt.title('Top 10 Netflix Genres')
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_1_Genres.png'))
plt.show()

# -------------------------------------

#  Top Producing Countries
# -------------------------------------
df_country = df.dropna(subset=["country"])
countries = df_country["country"].str.split(', ').explode()
top_countries = countries.value_counts().head(10)

plt.figure(figsize=(14, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="Set3")
plt.title('Top 10 Producing Countries on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_2_Countries.png'))
plt.show()
#-----------------------------
df_cast = df.dropna(subset=['cast'])
df_cast = df_cast.assign(cast=df_cast['cast'].str.split(', ')).explode('cast')
top_actors = df_cast['cast'].value_counts().head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_actors.values, y=top_actors.index, palette='coolwarm')
plt.title('Top 10 Most Frequent Actors in Netflix Titles')
plt.xlabel('Number of Titles')
plt.ylabel('Actor')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_3_Top_Actors.png'))
plt.show()

df_month = df.dropna(subset=['date_added'])
df_month['month_added'] = pd.to_datetime(df_month['date_added'], errors='coerce').dt.month_name()

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

month_counts = df_month['month_added'].value_counts().reindex(month_order)

plt.figure(figsize=(12, 6))
sns.barplot(x=month_counts.index, y=month_counts.values, palette='viridis')
plt.title('Titles Added by Month (Seasonality Pattern)')
plt.xlabel('Month')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_4_Monthly_Additions.png'))
plt.show()

# -------------------------------------
# Content Type Distribution
# -------------------------------------
type_counts = df["type"].value_counts()

plt.figure(figsize=(8, 6))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90,
        colors=["#ff9999", "#66b3ff"], textprops={'fontsize': 12})
plt.title("Distribution of Content Types on Netflix")
plt.axis('equal')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_4_Type_Distribution.png'))
plt.show()

# -------------------------------------
# Content Rating Distribution
# -------------------------------------
rating_counts = df['rating'].dropna().value_counts().head(8)

plt.figure(figsize=(8, 6))
plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140,
        colors=sns.color_palette("pastel"), textprops={'fontsize': 11})
plt.title("Top 8 Content Ratings Distribution")
plt.axis('equal')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_5_Rating_Distribution.png'))
plt.show()

# -------------------------------------
# Global Choropleth of Titles by Country
# -------------------------------------
country_counts = df['country'].dropna().str.split(', ').explode().value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Titles']
country_counts['Log Titles'] = country_counts['Number of Titles'].apply(lambda x: round(x**0.5, 2))

fig = px.choropleth(
    country_counts,
    locations='Country',
    locationmode='country names',
    color='Log Titles',
    hover_name='Country',
    hover_data={'Number of Titles': True},
    color_continuous_scale='sunsetdark',
    title=' Global Distribution of Netflix Titles',
    height=600
)
fig.update_geos(showcoastlines=True, projection_type='natural earth')
fig.write_html(os.path.join(out_dir, "Figure_6.1_Global_Choropleth.html"))

import plotly.express as px

# Prepare data
df_country = df.dropna(subset=["country"])
countries = df_country["country"].str.split(', ').explode()
top_countries = countries.value_counts().head(25).reset_index()
top_countries.columns = ['Country', 'Number of Titles']

# Plot with discrete color per country
fig = px.choropleth(
    top_countries,
    locations='Country',
    locationmode='country names',
    color='Country',
    hover_name='Country',
    hover_data={'Number of Titles': True},
    title='Top 25 Netflix-Producing Countries (Color-Coded)',
    height=600
)
fig.update_geos(showcoastlines=True, projection_type='natural earth')
fig.write_html(os.path.join(out_dir, "Figure_6.2_Countries_Discrete.html"))


# -------------------------------------

# -------------------------------------
# Titles Added per Year with Dots
# -------------------------------------
df['year_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year
df_year = df.dropna(subset=['year_added', 'type'])
yearly = df_year.groupby(['year_added', 'type']).size().reset_index(name='count')

line = alt.Chart(yearly).mark_line(strokeWidth=2).encode(
    x=alt.X('year_added:O', title='Year Added', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count:Q', title='Number of Titles'),
    color=alt.Color('type:N', title='Content Type', scale=alt.Scale(scheme='set1'))
)

points = alt.Chart(yearly).mark_point(filled=True, size=65, shape='circle').encode(
    x='year_added:O', y='count:Q', color='type:N', tooltip=['year_added', 'type', 'count']
)

(line + points).properties(
    width=720, height=420, title='Netflix Titles Added per Year by Type (with Dots)'
).interactive().save(os.path.join(out_dir, 'Figure_7_Yearly_Additions_With_Dots.html'))

print("\n All visualizations generated and saved successfully.")
# Extract year from date_added
df['year_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year
df_country_time = df.dropna(subset=["country", "year_added"])

# Normalize multiple countries per entry
df_country_time = df_country_time.assign(
    country=df_country_time['country'].str.split(', ')
).explode('country')

# Top 5 countries overall
top5_countries = df_country_time['country'].value_counts().nlargest(5).index
df_top5 = df_country_time[df_country_time['country'].isin(top5_countries)]

# Group by year and country
country_year = df_top5.groupby(['year_added', 'country']).size().reset_index(name='count')

# Plot
chart = alt.Chart(country_year).mark_line(point=True).encode(
    x=alt.X('year_added:O', title='Year'),
    y=alt.Y('count:Q', title='Number of Titles'),
    color=alt.Color('country:N', title='Country'),
    tooltip=['year_added', 'country', 'count']
).properties(
    width=700,
    height=400,
    title='Netflix Title Additions per Year (Top 5 Countries)'
).interactive()

chart_path = os.path.join(out_dir, 'Figure_8_Country_Trend.html')
chart.save(chart_path)
df_delay = df.dropna(subset=['release_year', 'date_added'])
df_delay['year_added'] = pd.to_datetime(df_delay['date_added'], errors='coerce').dt.year
df_delay['delay'] = df_delay['year_added'] - df_delay['release_year']
df_delay = df_delay[(df_delay['delay'] >= 0) & (df_delay['delay'] < 30)]

plt.figure(figsize=(10, 6))
sns.histplot(df_delay['delay'], bins=30, kde=True, color='darkblue')
plt.title('Time Between Content Release and Netflix Addition')
plt.xlabel('Years Delay')
plt.ylabel('Number of Titles')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'Figure_9_Release_Delay.png'))
plt.show()


def title_length_category(row):
    length = len(str(row['title']))
    if length < 15:
        return 'Short Title'
    elif length < 30:
        return 'Medium Title'
    else:
        return 'Long Title'

df['title_length_category'] = df.apply(title_length_category, axis=1)
# -------------------------------------
#  Number of Titles by Country (Netflix)
# -------------------------------------
country_counts = df['country'].dropna().str.split(', ').explode().value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Titles']
country_counts['Log Titles'] = country_counts['Number of Titles'].apply(lambda x: round(x**0.5, 2))

fig = px.choropleth(
    country_counts,
    locations='Country',
    locationmode='country names',
    color='Log Titles',
    hover_name='Country',
    hover_data={'Number of Titles': True},
    color_continuous_scale='sunsetdark',
    title=' Global Distribution of Netflix Titles',
    height=600
)
fig.update_geos(showcoastlines=True, projection_type='natural earth')
fig.write_html(os.path.join(out_dir, "Figure_10_Global_Choropleth.html"))
# Group and compute counts
source = df.groupby(['type', 'title_length_category']).size().reset_index(name='count')

# Order for visual clarity
title_order = ['Short Title', 'Medium Title', 'Long Title']

# Altair Faceted Bar Chart
alt.Chart(source).mark_bar().encode(
    x=alt.X('title_length_category:N', sort=title_order, axis=alt.Axis(title='Title Length')),
    y=alt.Y('count:Q', title='Number of Titles'),
    color=alt.Color('title_length_category:N', legend=None),
    tooltip=['title_length_category', 'count']
).properties(width=350, height=400).facet(
    column=alt.Column('type:N', title='Content Type')
).properties(
    title='Netflix Title Count by Title Length and Content Type'
).save(os.path.join(out_dir, 'Figure_11_Length_vs_Type.html'))
# Clean and filter
df_rated = df[['type', 'rating']].dropna()
df_rated = df_rated[df_rated['rating'] != 'NR']  # Optional: remove ambiguous ratings
top_ratings = df_rated['rating'].value_counts().nlargest(6).index
df_filtered = df_rated[df_rated['rating'].isin(top_ratings)]

# Group and compute counts
source = df_filtered.groupby(['type', 'rating']).size().reset_index(name='count')

# Altair Faceted Bar Chart
alt.Chart(source).mark_bar().encode(
    x=alt.X('rating:N', axis=alt.Axis(title='Rating', labelAngle=0)),
    y=alt.Y('count:Q', title='Number of Titles'),
    color=alt.Color('rating:N', legend=None),
    tooltip=['rating', 'count']
).properties(width=400, height=400).facet(
    column=alt.Column('type:N', title=None)
).properties(
    title='Top Ratings Distribution by Netflix Content Type'
).save(os.path.join(out_dir, 'Figure_12_Rating_vs_Type.html'))
import matplotlib.pyplot as plt
import seaborn as sns

#---------------------------------------

import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data as vg_data
import os

# Output folder
out_dir = r"C:\Users\14163\Desktop\university cu boulder\Fundamentals of Data Visualization\Data"
os.makedirs(out_dir, exist_ok=True)

# 🎲 Simulate fake Netflix counts for U.S. states
us_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

# Simulated title counts
np.random.seed(0)
fake_counts = np.random.randint(20, 500, size=len(us_states))

state_df = pd.DataFrame({'location': us_states, 'count': fake_counts})

#  Static mapping of state name to FIPS ID
name_to_fips = {
    'Alabama': 1, 'Alaska': 2, 'Arizona': 4, 'Arkansas': 5, 'California': 6, 'Colorado': 8,
    'Connecticut': 9, 'Delaware': 10, 'Florida': 12, 'Georgia': 13, 'Hawaii': 15, 'Idaho': 16,
    'Illinois': 17, 'Indiana': 18, 'Iowa': 19, 'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22,
    'Maine': 23, 'Maryland': 24, 'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27,
    'Mississippi': 28, 'Missouri': 29, 'Montana': 30, 'Nebraska': 31, 'Nevada': 32,
    'New Hampshire': 33, 'New Jersey': 34, 'New Mexico': 35, 'New York': 36,
    'North Carolina': 37, 'North Dakota': 38, 'Ohio': 39, 'Oklahoma': 40, 'Oregon': 41,
    'Pennsylvania': 42, 'Rhode Island': 44, 'South Carolina': 45, 'South Dakota': 46,
    'Tennessee': 47, 'Texas': 48, 'Utah': 49, 'Vermont': 50, 'Virginia': 51,
    'Washington': 53, 'West Virginia': 54, 'Wisconsin': 55, 'Wyoming': 56
}

# Assign FIPS ID
state_df['id'] = state_df['location'].map(name_to_fips)
state_df.dropna(inplace=True)
state_df['id'] = state_df['id'].astype(int)

#  Load U.S. map
states = alt.topo_feature(vg_data.us_10m.url, 'states')

# Choropleth map
chart = alt.Chart(states).mark_geoshape().encode(
    color=alt.Color('count:Q', title='Simulated Netflix Titles', scale=alt.Scale(scheme='blues')),
    tooltip=[
        alt.Tooltip('location:N', title='State'),
        alt.Tooltip('count:Q', title='Simulated Titles')
    ]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(state_df, key='id', fields=['location', 'count'])
).project(
    type='albersUsa'
).properties(
    width=600,
    height=400,
    title='Simulated Netflix Title Count by U.S. State'
)

# Save to HTML
chart.save(os.path.join(out_dir, 'Figure_13_US_Choropleth.html'))






