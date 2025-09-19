# Part 1 — Data Loading and Basic Exploration
# analysis.py
import pandas as pd

# Load CSV
df = pd.read_csv('metadata.csv')

# Show first rows
print(df.head())

# Basic info
print(df.shape)
print(df.info())

# Missing values
print(df.isnull().sum())


# Part 2 — Data Cleaning and Preparation
# Drop rows without publish_time or title
df = df.dropna(subset=['publish_time','title'])

# Convert publish_time to datetime
df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

# Extract year
df['year'] = df['last_updated'].dt.year

# Create word count column for abstract
df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))


# Part 3 — Analysis and Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Publications by year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,4))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title('Publications by Year')
plt.show()

# Top 10 journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(8,4))
sns.barplot(y=top_journals.index, x=top_journals.values)
plt.title('Top Publishing Journals')
plt.show()

