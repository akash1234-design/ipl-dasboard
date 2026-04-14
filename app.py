st.write(df.columns)
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IPL Dashboard", layout="wide")

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("matches.csv")
    return df
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    
    return df

df = load_data()

# ==============================
# TITLE
# ==============================
st.title("🏏 IPL Data Analysis Dashboard")

# ==============================
# DEBUG (remove later)
# ==============================
st.write("Columns:", df.columns)

# ==============================
# SAFE COLUMN HANDLING
# ==============================
if 'season' not in df.columns:
    st.error("❌ 'season' column missing in dataset")
    st.stop()

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("Filters")

seasons = sorted(df['season'].dropna().unique())
selected_season = st.sidebar.selectbox("Select Season", seasons)

filtered_df = df[df['season'] == selected_season]

# ==============================
# METRICS
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Matches", len(filtered_df))

with col2:
    if 'team1' in df.columns:
        st.metric("Teams", filtered_df['team1'].nunique())

with col3:
    if 'winner' in df.columns:
        st.metric("Winners", filtered_df['winner'].nunique())

# ==============================
# DATA TABLE
# ==============================
st.subheader("📊 Match Data")
st.dataframe(filtered_df)

# ==============================
# TOP TEAMS
# ==============================
if 'winner' in df.columns:
    st.subheader("🏆 Most Winning Teams")
    win_count = filtered_df['winner'].value_counts()
    st.bar_chart(win_count)

# ==============================
# DOWNLOAD OPTION
# ==============================
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Data",
    data=csv,
    file_name="ipl_filtered_data.csv",
    mime="text/csv"
)
