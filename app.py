# ============================================================
# 🏏 IPL PREMIUM DASHBOARD
# No API needed | Pure Python + Pandas + Plotly
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}
.stApp { background-color: #0a0a0a; }

.hero {
    background: linear-gradient(135deg, #FF6B00 0%, #cc4400 40%, #1a0a4a 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(255,107,0,0.3);
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.8rem;
    letter-spacing: 6px;
    color: #fff;
    margin: 0;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.hero p { color: #ffcc99; font-size: 1rem; margin-top: 0.5rem; }

.metric-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #FF6B00;
    border-radius: 16px;
    padding: 1.3rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(255,107,0,0.15);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(255,107,0,0.3); }
.metric-number { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: #FF6B00; }
.metric-label { color: #aaa; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }

.cap-card-orange {
    background: linear-gradient(135deg, #FF6B00, #ff9500);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(255,107,0,0.4);
}
.cap-card-purple {
    background: linear-gradient(135deg, #6b00ff, #9500ff);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(107,0,255,0.4);
}
.cap-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 3px; color: #fff; }
.cap-player { font-size: 1.6rem; font-weight: 700; color: #fff; margin: 0.5rem 0; }
.cap-stat { font-size: 1rem; color: rgba(255,255,255,0.85); }

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #FF6B00;
    letter-spacing: 3px;
    border-left: 4px solid #FF6B00;
    padding-left: 12px;
    margin: 1.5rem 0 1rem 0;
}

[data-testid="stSidebar"] { background-color: #0d0d1a !important; border-right: 1px solid #FF6B00; }
.stTabs [data-baseweb="tab-list"] { background-color: #1a1a2e; border-radius: 10px; }
.stTabs [aria-selected="true"] { color: #FF6B00 !important; border-bottom: 2px solid #FF6B00; }
.stTabs [data-baseweb="tab"] { color: #aaa; }

.stButton > button {
    background: linear-gradient(135deg, #FF6B00, #cc4400);
    color: white; border: none; border-radius: 10px;
    font-weight: 700; padding: 0.6rem 2rem;
    transition: all 0.2s; letter-spacing: 1px;
}
.stButton > button:hover { transform: scale(1.03); box-shadow: 0 4px 15px rgba(255,107,0,0.4); }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    matches.columns = matches.columns.str.strip().str.lower()
    deliveries.columns = deliveries.columns.str.strip().str.lower()
    return matches, deliveries

matches, deliveries = load_data()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🏏 IPL DASHBOARD</h1>
    <p>Indian Premier League • Stats • Analysis • Records</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏏 IPL Filters")
    st.markdown("---")

    seasons = sorted(matches["season"].dropna().unique().tolist(), reverse=True)
    sel_season = st.selectbox("📅 Season", ["All Seasons"] + [str(s) for s in seasons])

    if "team1" in matches.columns:
        all_teams = sorted(set(matches["team1"].dropna().tolist() + matches["team2"].dropna().tolist()))
        sel_team = st.selectbox("🏟️ Team", ["All Teams"] + all_teams)
    else:
        sel_team = "All Teams"

    if "city" in matches.columns:
        cities = sorted(matches["city"].dropna().unique().tolist())
        sel_city = st.selectbox("🌆 City", ["All Cities"] + cities)
    else:
        sel_city = "All Cities"

    st.markdown("---")
    st.markdown(f"### 📊 Dataset\n**Matches:** {len(matches)}\n\n**Deliveries:** {len(deliveries)}")

# ── Filter Data ───────────────────────────────────────────────────────────────
filt = matches.copy()
if sel_season != "All Seasons":
    filt = filt[filt["season"].astype(str) == sel_season]
if sel_team != "All Teams" and "team1" in filt.columns:
    filt = filt[(filt["team1"] == sel_team) | (filt["team2"] == sel_team)]
if sel_city != "All Cities" and "city" in filt.columns:
    filt = filt[filt["city"] == sel_city]

# Filtered deliveries
if sel_season != "All Seasons" and "match_id" in deliveries.columns and "id" in filt.columns:
    filt_del = deliveries[deliveries["match_id"].isin(filt["id"])]
else:
    filt_del = deliveries.copy()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
total_matches = len(filt)
total_seasons = filt["season"].nunique() if "season" in filt.columns else 0
total_teams   = len(set(filt["team1"].dropna().tolist() + filt["team2"].dropna().tolist())) if "team1" in filt.columns else 0
total_runs    = filt_del["total_runs"].sum() if "total_runs" in filt_del.columns else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{total_matches}</div><div class="metric-label">Total Matches</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{total_seasons}</div><div class="metric-label">Seasons</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{total_teams}</div><div class="metric-label">Teams</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-number">{int(total_runs):,}</div><div class="metric-label">Total Runs</div></div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Overview",
    "🧢 Orange & Purple Cap",
    "📈 Trends",
    "🏟️ Team Stats",
    "🔍 Match Explorer"
])

ORANGE = "#FF6B00"
PURPLE = "#6b00ff"
PLOT_BG = "rgba(0,0,0,0)"
FONT_C  = "#ffffff"

def dark_fig(fig):
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(color=FONT_C),
        xaxis=dict(gridcolor="#222", zerolinecolor="#222"),
        yaxis=dict(gridcolor="#222", zerolinecolor="#222"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_C)),
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    # Most wins
    with col1:
        st.markdown('<div class="section-title">🏆 MOST WINS</div>', unsafe_allow_html=True)
        if "winner" in filt.columns:
            wins = filt["winner"].dropna().value_counts().head(10)
            fig = px.bar(x=wins.values, y=wins.index, orientation="h",
                         color=wins.values,
                         color_continuous_scale=["#cc4400", ORANGE, "#ffcc00"],
                         labels={"x": "Wins", "y": ""})
            fig.update_layout(coloraxis_showscale=False)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

    # Toss decisions
    with col2:
        st.markdown('<div class="section-title">🪙 TOSS DECISIONS</div>', unsafe_allow_html=True)
        if "toss_decision" in filt.columns:
            td = filt["toss_decision"].value_counts()
            fig2 = px.pie(values=td.values, names=td.index,
                          color_discrete_sequence=[ORANGE, PURPLE])
            fig2.update_traces(textfont_color="white")
            dark_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)

    # Player of the match
    st.markdown('<div class="section-title">⭐ TOP PLAYER OF THE MATCH</div>', unsafe_allow_html=True)
    if "player_of_match" in filt.columns:
        pom = filt["player_of_match"].dropna().value_counts().head(10)
        fig3 = px.bar(x=pom.index, y=pom.values,
                      color=pom.values,
                      color_continuous_scale=["#cc4400", ORANGE, "#ffcc00"],
                      labels={"x": "Player", "y": "Awards"})
        fig3.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        dark_fig(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    # Venue
    if "venue" in filt.columns:
        st.markdown('<div class="section-title">🏟️ TOP VENUES</div>', unsafe_allow_html=True)
        venues = filt["venue"].dropna().value_counts().head(8)
        fig4 = px.bar(x=venues.values, y=venues.index, orientation="h",
                      color=venues.values,
                      color_continuous_scale=["#1a0a4a", PURPLE, ORANGE],
                      labels={"x": "Matches", "y": ""})
        fig4.update_layout(coloraxis_showscale=False)
        dark_fig(fig4)
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ORANGE & PURPLE CAP
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">🧢 ORANGE CAP & PURPLE CAP</div>', unsafe_allow_html=True)

    cap_col1, cap_col2 = st.columns(2)

    # Orange Cap — Most Runs
    with cap_col1:
        if "batsman" in filt_del.columns and "batsman_runs" in filt_del.columns:
            orange_cap = filt_del.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(1)
            orange_name = orange_cap.index[0]
            orange_runs = int(orange_cap.values[0])
            st.markdown(f"""
            <div class="cap-card-orange">
                <div class="cap-title">🟠 ORANGE CAP</div>
                <div class="cap-player">🏏 {orange_name}</div>
                <div class="cap-stat">Most Runs: <b>{orange_runs:,}</b></div>
            </div>
            """, unsafe_allow_html=True)

            # Top 10 run scorers
            top_runs = filt_del.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(10)
            fig = px.bar(x=top_runs.values, y=top_runs.index, orientation="h",
                         color=top_runs.values,
                         color_continuous_scale=["#cc4400", ORANGE, "#ffcc00"],
                         labels={"x": "Runs", "y": "Batsman"})
            fig.update_layout(coloraxis_showscale=False, title="Top 10 Run Scorers",
                              title_font_color=FONT_C)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Batsman data nahi mila deliveries CSV mein.")

    # Purple Cap — Most Wickets
    with cap_col2:
        wicket_cols = [c for c in filt_del.columns if "wicket" in c or "dismissal" in c or "bowler" in c]

        if "bowler" in filt_del.columns and "dismissal_kind" in filt_del.columns:
            wickets_df = filt_del[filt_del["dismissal_kind"].notna() &
                                   (~filt_del["dismissal_kind"].isin(["run out","retired hurt","obstructing the field"]))]
            purple_cap = wickets_df.groupby("bowler").size().sort_values(ascending=False).head(1)
            purple_name = purple_cap.index[0]
            purple_wkts = int(purple_cap.values[0])
            st.markdown(f"""
            <div class="cap-card-purple">
                <div class="cap-title">🟣 PURPLE CAP</div>
                <div class="cap-player">🎳 {purple_name}</div>
                <div class="cap-stat">Most Wickets: <b>{purple_wkts}</b></div>
            </div>
            """, unsafe_allow_html=True)

            top_wickets = wickets_df.groupby("bowler").size().sort_values(ascending=False).head(10)
            fig2 = px.bar(x=top_wickets.values, y=top_wickets.index, orientation="h",
                          color=top_wickets.values,
                          color_continuous_scale=["#1a0a4a", PURPLE, "#cc99ff"],
                          labels={"x": "Wickets", "y": "Bowler"})
            fig2.update_layout(coloraxis_showscale=False, title="Top 10 Wicket Takers",
                               title_font_color=FONT_C)
            dark_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Bowler/dismissal data nahi mila.")

    # Strike Rate & Economy
    st.markdown('<div class="section-title">📊 BATTING & BOWLING STATS</div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)

    with s1:
        if "batsman" in filt_del.columns and "batsman_runs" in filt_del.columns:
            bat_stats = filt_del.groupby("batsman").agg(
                runs=("batsman_runs", "sum"),
                balls=("ball", "count")
            ).reset_index()
            bat_stats = bat_stats[bat_stats["balls"] >= 100]
            bat_stats["strike_rate"] = (bat_stats["runs"] / bat_stats["balls"] * 100).round(2)
            top_sr = bat_stats.sort_values("strike_rate", ascending=False).head(10)
            fig = px.bar(x=top_sr["strike_rate"], y=top_sr["batsman"], orientation="h",
                         color=top_sr["strike_rate"],
                         color_continuous_scale=["#cc4400", ORANGE],
                         labels={"x": "Strike Rate", "y": ""})
            fig.update_layout(coloraxis_showscale=False, title="Best Strike Rates (min 100 balls)",
                              title_font_color=FONT_C)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

    with s2:
        if "bowler" in filt_del.columns and "total_runs" in filt_del.columns:
            bowl_stats = filt_del.groupby("bowler").agg(
                runs=("total_runs", "sum"),
                balls=("ball", "count")
            ).reset_index()
            bowl_stats = bowl_stats[bowl_stats["balls"] >= 120]
            bowl_stats["economy"] = (bowl_stats["runs"] / (bowl_stats["balls"] / 6)).round(2)
            top_eco = bowl_stats.sort_values("economy").head(10)
            fig2 = px.bar(x=top_eco["economy"], y=top_eco["bowler"], orientation="h",
                          color=top_eco["economy"],
                          color_continuous_scale=["#6b00ff", PURPLE],
                          labels={"x": "Economy", "y": ""})
            fig2.update_layout(coloraxis_showscale=False, title="Best Economy (min 20 overs)",
                               title_font_color=FONT_C)
            dark_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">📈 IPL TRENDS</div>', unsafe_allow_html=True)

    trend_opts = []
    if "season" in matches.columns: trend_opts += ["Matches Per Season", "Runs Per Season"]
    if "toss_decision" in matches.columns: trend_opts += ["Toss Decision Trend"]
    if "winner" in matches.columns and "toss_winner" in matches.columns: trend_opts += ["Toss Win = Match Win?"]

    if trend_opts:
        sel_trend = st.selectbox("Trend choose karo:", trend_opts)

        if sel_trend == "Matches Per Season":
            data = matches["season"].value_counts().sort_index()
            fig = px.area(x=data.index.astype(str), y=data.values,
                          labels={"x": "Season", "y": "Matches"},
                          color_discrete_sequence=[ORANGE])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(255,107,0,0.15)", line_color=ORANGE, line_width=3)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

        elif sel_trend == "Runs Per Season" and "match_id" in deliveries.columns and "id" in matches.columns:
            season_map = matches.set_index("id")["season"].to_dict()
            deliveries["season"] = deliveries["match_id"].map(season_map)
            runs_season = deliveries.groupby("season")["total_runs"].sum().sort_index()
            fig = px.bar(x=runs_season.index.astype(str), y=runs_season.values,
                         color=runs_season.values,
                         color_continuous_scale=["#cc4400", ORANGE, "#ffcc00"],
                         labels={"x": "Season", "y": "Total Runs"})
            fig.update_layout(coloraxis_showscale=False)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

        elif sel_trend == "Toss Decision Trend":
            td = matches.groupby(["season", "toss_decision"]).size().reset_index(name="count")
            fig = px.line(td, x="season", y="count", color="toss_decision",
                          color_discrete_map={"bat": ORANGE, "field": PURPLE},
                          markers=True)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

        elif sel_trend == "Toss Win = Match Win?":
            matches["toss_match_win"] = matches["toss_winner"] == matches["winner"]
            result = matches["toss_match_win"].value_counts()
            labels = ["Toss + Match Win", "Toss Win but Match Lost"]
            fig = px.pie(values=result.values, names=labels,
                         color_discrete_sequence=[ORANGE, PURPLE])
            fig.update_traces(textfont_color="white")
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TEAM STATS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🏟️ TEAM STATISTICS</div>', unsafe_allow_html=True)

    if "winner" in matches.columns and "team1" in matches.columns:
        all_teams_list = sorted(set(matches["team1"].dropna().tolist() + matches["team2"].dropna().tolist()))
        sel_t = st.selectbox("Team select karo:", all_teams_list, key="team_sel")

        team_matches = matches[(matches["team1"] == sel_t) | (matches["team2"] == sel_t)]
        team_wins    = matches[matches["winner"] == sel_t]
        win_pct      = round(len(team_wins) / len(team_matches) * 100, 1) if len(team_matches) > 0 else 0

        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown(f'<div class="metric-card"><div class="metric-number">{len(team_matches)}</div><div class="metric-label">Matches Played</div></div>', unsafe_allow_html=True)
        with tc2:
            st.markdown(f'<div class="metric-card"><div class="metric-number">{len(team_wins)}</div><div class="metric-label">Matches Won</div></div>', unsafe_allow_html=True)
        with tc3:
            st.markdown(f'<div class="metric-card"><div class="metric-number">{win_pct}%</div><div class="metric-label">Win Rate</div></div>', unsafe_allow_html=True)

        # Win per season
        if "season" in team_wins.columns:
            wins_season = team_wins["season"].value_counts().sort_index()
            fig = px.bar(x=wins_season.index.astype(str), y=wins_season.values,
                         color=wins_season.values,
                         color_continuous_scale=["#cc4400", ORANGE],
                         labels={"x": "Season", "y": "Wins"},
                         title=f"{sel_t} — Wins Per Season")
            fig.update_layout(coloraxis_showscale=False, title_font_color=FONT_C)
            dark_fig(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Top players of match for team
        if "player_of_match" in team_matches.columns:
            pom = team_matches["player_of_match"].dropna().value_counts().head(8)
            fig2 = px.bar(x=pom.values, y=pom.index, orientation="h",
                          color=pom.values,
                          color_continuous_scale=["#1a0a4a", PURPLE, ORANGE],
                          labels={"x": "Awards", "y": "Player"},
                          title=f"{sel_t} — Top Players of Match")
            fig2.update_layout(coloraxis_showscale=False, title_font_color=FONT_C)
            dark_fig(fig2)
            st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MATCH EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🔍 MATCH EXPLORER</div>', unsafe_allow_html=True)

    search_q = st.text_input("🔎 Search karo — team, player, city, venue...",
                              placeholder="e.g. Mumbai, Kohli, Wankhede...")

    searchable = [c for c in ["team1","team2","winner","player_of_match","city","venue","toss_winner"] if c in filt.columns]
    search_in  = st.multiselect("Kahan search karein?", searchable, default=searchable[:3])

    display_df = filt.copy()

    if search_q and search_in:
        mask = pd.Series([False] * len(filt))
        for col in search_in:
            mask |= filt[col].astype(str).str.contains(search_q, case=False, na=False)
        display_df = filt[mask]
        st.success(f"✅ **{len(display_df)} matches** mile!")
    
    show_cols = [c for c in ["season","date","team1","team2","winner","player_of_match","city","venue","toss_decision"] if c in display_df.columns]
    st.dataframe(display_df[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True, height=450)

    csv_data = display_df[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download as CSV", csv_data, "ipl_filtered.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p style="text-align:center; color:#555; font-size:0.8rem;">🏏 IPL Dashboard | Built with Streamlit & Plotly</p>', unsafe_allow_html=True)
