# Step 0: Install missing packages
import sys
import subprocess
import os

def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["pandas", "altair", "altair_viewer", "matplotlib", "seaborn"]:
    install_if_missing(pkg)

# Step 1: Import libraries
import pandas as pd
import altair as alt
import altair_viewer
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load dataset
file_path = r"C:\Users\14163\Desktop\university cu boulder\Fundamentals of Data Visualization\Data\netflix_titles.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ File not found: {file_path}")

df = pd.read_csv(file_path)

# Output directory
out_dir = r"C:\Users\14163\Desktop\university cu boulder\Fundamentals of Data Visualization\Data"
os.makedirs(out_dir, exist_ok=True)

# ---------------- 1. Top 10 Netflix Genres ----------------
genres = df['listed_in'].dropna().str.split(', ')
genres_exploded = genres.explode()
top_genres = genres_exploded.value_counts().head(10)

plt.figure(figsize=(14, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette="Set2")
plt.title('Top 10 Netflix Genres')
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
plt.tight_layout()
genre_path = os.path.join(out_dir, 'Figure_1_Genres.png')
plt.savefig(genre_path)
plt.show()
os.startfile(genre_path)

# ---------------- 2. Netflix Titles by Year and Type (Altair) ----------------
df_clean = df.dropna(subset=["release_year", "type"])
df_clean["release_year"] = df_clean["release_year"].astype(int)
yearly_counts = df_clean.groupby(["release_year", "type"]).size().reset_index(name="count")

line_chart = alt.Chart(yearly_counts).mark_line(point=True).encode(
    x=alt.X("release_year:O", title="Release Year", axis=alt.Axis(labelAngle=-45, labelOverlap=True, labelFontSize=10)),
    y=alt.Y("count:Q", title="Number of Titles"),
    color=alt.Color("type:N", title="Content Type"),
    tooltip=["release_year", "type", "count"]
).properties(
    width=700,
    height=400,
    title="Netflix Titles by Year and Type"
).interactive()

line_chart_path = os.path.join(out_dir, 'Figure_2_Type_Year.html')
line_chart.save(line_chart_path)
altair_viewer.display(line_chart)
os.startfile(line_chart_path)

# ---------------- 3. Top Producing Countries ----------------
df_country = df.dropna(subset=["country"])
countries = df_country["country"].str.split(', ').explode()
top_countries = countries.value_counts().head(10)

plt.figure(figsize=(14, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="Set3")
plt.title('Top 10 Producing Countries on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.tight_layout()
country_path = os.path.join(out_dir, 'Figure_3_Countries.png')
plt.savefig(country_path)
plt.show()
os.startfile(country_path)

# ---------------- 4. Content Type Distribution (Movie vs TV Show) ----------------
type_counts = df["type"].value_counts()

plt.figure(figsize=(8, 6))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90,
        colors=["#ff9999", "#66b3ff"], textprops={'fontsize': 12})
plt.title("Distribution of Content Types on Netflix")
plt.axis('equal')
plt.tight_layout()
type_pie_path = os.path.join(out_dir, 'Figure_4_Type_Distribution.png')
plt.savefig(type_pie_path)
plt.show()
os.startfile(type_pie_path)

# ---------------- 5. Content Rating Distribution ----------------
df_rating = df.dropna(subset=["rating"])
rating_counts = df_rating["rating"].value_counts().head(8)

plt.figure(figsize=(8, 6))
plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140,
        colors=sns.color_palette("pastel"), textprops={'fontsize': 11})
plt.title("Top 8 Content Ratings Distribution")
plt.axis('equal')
plt.tight_layout()
rating_path = os.path.join(out_dir, 'Figure_5_Rating_Distribution.png')
plt.savefig(rating_path)
plt.show()
os.startfile(rating_path)

print("\n✅ All 5 visualizations completed and saved successfully.")
# 6. Improved Line Chart (Save also as PNG using Selenium)
improved_line_chart = alt.Chart(yearly_counts).mark_line(point=True).encode(
    x=alt.X("release_year:O", title="Release Year", axis=alt.Axis(labelAngle=-45, labelFontSize=10, labelOverlap=False)),
    y=alt.Y("count:Q", title="Number of Titles"),
    color=alt.Color("type:N", title="Content Type"),
    tooltip=["release_year", "type", "count"]
).properties(
    width=800,
    height=400,
    title="Netflix Titles by Year and Type (Improved)"
).interactive()

improved_line_chart_path_html = os.path.join(out_dir, 'Figure_6_Improved_LineChart.html')
improved_line_chart.save(improved_line_chart_path_html)
os.startfile(improved_line_chart_path_html)
altair_viewer.display(improved_line_chart)

# 7. Duration Analysis (Bar plot for simplicity)
df_duration = df.dropna(subset=["duration", "type"])
df_duration["duration_num"] = df_duration["duration"].str.extract("(\d+)").astype(float)
df_duration = df_duration[df_duration["duration_num"] < 300]  # filter outliers if needed

plt.figure(figsize=(10, 6))
sns.boxplot(x="type", y="duration_num", data=df_duration, palette="Set1")
plt.title("Distribution of Duration by Content Type")
plt.xlabel("Content Type")
plt.ylabel("Duration (Minutes or Seasons)")
plt.tight_layout()
duration_path = os.path.join(out_dir, 'Figure_7_Duration_Distribution.png')
plt.savefig(duration_path)
plt.show()
os.startfile(duration_path)
