import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="IPL Dashboard", layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #0e1117;
    color: white;
}

/* Sidebar fix */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# Title
st.title("🏏 IPL Match Analysis Dashboard")

# -------------------------------
# ✅ LOAD REAL DATA (NO BUG)
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ipl_data.csv")
    return df

df = load_data()

# Debug check (temporary)
st.write("Available Seasons:", sorted(df['season'].unique()))

# -------------------------------
# ✅ SIDEBAR FILTERS
# -------------------------------
st.sidebar.markdown("## ⚙️ Filter Options")

# 1. Season Selector
# Season ko string banaya taaki sort karne mein error na aaye
df['season'] = df['season'].astype(str)

season = st.sidebar.selectbox(
    "🏏 Select Season",
    sorted(df['season'].dropna().unique(), reverse=True)
)

# Filter data
filtered_df = df[df['season'] == season]

# -------------------------------
# ✅ TOP CARDS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Matches", len(filtered_df))

with col2:
    st.metric("Venues", filtered_df['venue'].nunique())

with col3:
    st.metric("Top Winner", filtered_df['winner'].mode()[0])

st.divider()

# -------------------------------
# ✅ MATCHES WON CHART
# -------------------------------
st.subheader(f"Matches Won in {season}")

win_count = filtered_df['winner'].value_counts().reset_index()
win_count.columns = ['Team', 'Wins']

fig = px.bar(win_count, x='Team', y='Wins', color='Team')
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# ✅ TOSS IMPACT
# -------------------------------
st.subheader("Toss Impact")

toss_win = filtered_df[filtered_df['toss_winner'] == filtered_df['winner']]

labels = ['Won Toss & Won Match', 'Lost Toss but Won Match']
values = [len(toss_win), len(filtered_df) - len(toss_win)]

fig2 = px.pie(names=labels, values=values)
st.plotly_chart(fig2)

# -------------------------------
# ✅ TOP PLAYERS
# -------------------------------
st.subheader("Top Players (Man of the Match)")

player_stats = df['player_of_match'].value_counts().reset_index()
player_stats.columns = ['Player', 'Awards']

fig3 = px.bar(player_stats.head(10), x='Player', y='Awards', color='Player')
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# ✅ VENUE ANALYSIS
# -------------------------------
st.subheader("Venue Analysis")

venue_count = filtered_df['venue'].value_counts().reset_index()
venue_count.columns = ['Venue', 'Matches']

fig4 = px.bar(venue_count, x='Venue', y='Matches')
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# ✅ POINTS TABLE
# -------------------------------
st.subheader("Points Table")

points = filtered_df['winner'].value_counts().reset_index()
points.columns = ['Team', 'Wins']
points['Points'] = points['Wins'] * 2

st.dataframe(points)

# -------------------------------
# ✅ DOWNLOAD BUTTON
# -------------------------------
st.download_button("Download Data", filtered_df.to_csv(index=False), "ipl_data.csv")
st.subheader("Team vs Team Analysis")

team1 = st.selectbox("Select Team 1", df['team1'].unique())
team2 = st.selectbox("Select Team 2", df['team2'].unique())

h2h = df[((df['team1'] == team1) & (df['team2'] == team2))] ((df['team1'] == team2) & (df['team2'] == team1))

st.write(f"Total Matches: {len(h2h)}")

if not h2h.empty:
    st.write(h2h['winner'].value_counts())
st.markdown(f"""
<div style='background:#111827;padding:20px;border-radius:15px;text-align:center;color:white'>
<h3>Total Matches</h3>
<h1>{len(filtered_df)}</h1>
</div>
""", unsafe_allow_html=True)

import os
