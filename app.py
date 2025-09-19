import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Load the dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    # Convert last_updated to datetime and extract year
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    df['year'] = df['last_updated'].dt.year
    # Add abstract word count for analysis
    df['description_word_count'] = df['description'].fillna('').apply(lambda x: len(x.split()))
    return df

df = load_data()

# --- App Layout ---
st.title("CORD-19 Research Papers Explorer")
st.write("An interactive dashboard for exploring COVID-19 research metadata")

# --- Show sample data ---
st.subheader("Sample Data")
st.dataframe(df.head())

# --- Publication trend by year ---
st.subheader("Publications by Year")
year_counts = df['year'].value_counts().sort_index()

fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Publications")
ax1.set_title("Number of Publications Over Time")
st.pyplot(fig1)

# --- Top source organizations ---
st.subheader("Top Publishing Organizations")
top_sources = df['source_organization'].value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(top_sources.index, top_sources.values)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Source Organization")
ax2.set_title("Top 10 Publishing Organizations")
st.pyplot(fig2)

# --- Interactive filter by year ---
st.subheader("Filter Papers by Year")
years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox("Select Year", years)

filtered = df[df['year'] == selected_year]
st.write(f"Found {len(filtered)} papers from {selected_year}:")
st.dataframe(filtered[['paper_title', 'author_list', 'source_organization']].head(10))
