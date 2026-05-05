# IPL Dashboard 🏏 | 2008-2024

Interactive Streamlit dashboard for complete IPL match analysis from 2008 to 2024. Explore 17 seasons, 1095 matches, and every stat that matters.

### 🚀 Live Demo
**[Click Here to Launch Dashboard](https://ipl-dashboard-link.streamlit.app)** ← apna link yaha daal dena

### 📸 Dashboard Preview
![IPL Dashboard](dashboard-screenshot.png) ← ye screenshot upload karke naam daal dena

### 📊 Dashboard Stats
- **1095** Total Matches Analyzed
- **17** Seasons (2008-2024)
- **19** Teams Covered  
- **36** Cities & Venues

### 🔥 Key Features

**1. Overview Tab** 
- Most wins by team with visual charts
- Toss decision analysis - Bat first vs Field first impact

**2. Orange & Purple Cap** 
- Season-wise top run scorers & wicket takers
- Historical Orange/Purple cap holders

**3. Trends Tab**
- Season-wise match trends and team performance over years
- Runs per season, wickets per season analysis

**4. Team Stats**
- Head-to-head records between any 2 teams
- Win % at home vs away venues
- Filter by team, season, city

**5. Explorer**
- Custom filters: Season, Team, City
- Deep dive into any specific match data

### 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Dataset**: matches.csv - 1095 IPL matches (2008-2024)

### 💡 Business Questions This Dashboard Answers
1. Does winning the toss actually help win the match? Check `Toss Decision` chart
2. Which team dominates at Wankhede Stadium?
3. Who is the most consistent Orange Cap contender across seasons?
4. Year-wise trend: Are IPL scores increasing every season?

### 💻 Run Locally
```bash
git clone https://github.com/akash1234-design/ipl-dashboard
cd ipl-dashboard
pip install -r requirements.txt
streamlit run app.py
