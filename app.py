import streamlit as st
import pandas as pd
from pathlib import Path

from utils.style import load_style


# ==========================
# CONFIG
# ==========================

ROOT = Path(__file__).parent

LOGO = ROOT / "assets" / "logo.png"


st.set_page_config(
    page_title="IPL InsightXI",
    page_icon=str(LOGO) if LOGO.exists() else "🏏",
    layout="wide"
)


load_style()



# ==========================
# LOAD DATA
# ==========================


@st.cache_data
def load_data():

    matches = pd.read_csv(
        ROOT/"data"/"matches.csv"
    )

    deliveries = pd.read_csv(
        ROOT/"data"/"deliveries.csv"
    )

    return matches, deliveries



matches, deliveries = load_data()



# ==========================
# SIDEBAR BRAND
# ==========================


with st.sidebar:


    if LOGO.exists():

        st.image(
            str(LOGO),
            width=150
        )


    st.markdown(

    """

<h2 style="
color:white;
text-align:center;
">

IPL InsightXI

</h2>


<p style="
color:#94a3b8;
text-align:center;
">

Cricket Analytics Platform

</p>

    """,

    unsafe_allow_html=True

    )



    st.divider()



    st.markdown(

    """

<p style="
color:#cbd5e1;
font-size:15px;
">

Explore IPL through:

<br><br>

🏏 Match Prediction

<br>
🏆 Team Analysis

<br>
👤 Player Intelligence

<br>
🏟 Venue Analytics

</p>

    """,

    unsafe_allow_html=True

    )





# ==========================
# STATS
# ==========================


teams=len(

set(matches.team1)

.union(

set(matches.team2)

)

)



players=deliveries.batsman.nunique()


seasons=matches.season.nunique()


total_matches=len(matches)




runs=(

deliveries

.groupby("batsman")

.batsman_runs

.sum()

.sort_values(

ascending=False

)

)


top_player=runs.index[0]

top_runs=int(runs.iloc[0])



wins=matches.winner.value_counts()


best_team=wins.index[0]

best_wins=int(wins.iloc[0])



best_venue=matches.venue.value_counts().index[0]




# ==========================
# HERO
# ==========================


logo_html=""


if LOGO.exists():

    logo_html=f"""

<img src="data:image/png;base64,{open(LOGO,'rb').read().encode('base64') if False else ''}">

"""



st.markdown(

"""

<div class="hero">


<div style="text-align:center;">


<h1 style="
font-size:60px;
color:white;
">

🏏 IPL InsightXI

</h1>


<h2 style="
color:#38BDF8;
">

AI Powered IPL Analytics Platform

</h2>


<p style="
font-size:20px;
color:#cbd5e1;
">

Discover IPL history through prediction,
statistics and intelligent insights.

</p>


</div>


</div>

""",

unsafe_allow_html=True

)



# Display logo separately (safe)

if LOGO.exists():

    col1,col2,col3=st.columns([2,1,2])

    with col2:

        st.image(
            str(LOGO),
            width=180
        )





# ==========================
# KPI
# ==========================


st.markdown(
"## 📊 IPL Universe"
)



c1,c2,c3,c4=st.columns(4)



data=[

("Matches",total_matches),

("Teams",teams),

("Players",players),

("Seasons",seasons)

]



for col,(title,value) in zip(

[c1,c2,c3,c4],

data

):

    col.markdown(

    f"""

<div class="card">


<h1>

{value:,}

</h1>


<p>

{title}

</p>


</div>

""",

unsafe_allow_html=True

    )





# ==========================
# INSIGHTS
# ==========================


st.divider()


st.markdown(
"## 🔥 IPL Insights"
)



a,b,c=st.columns(3)



cards=[

(
"Top Run Scorer",
top_player,
f"{top_runs:,} Runs"
),

(
"Most Successful Team",
best_team,
f"{best_wins} Wins"
),

(
"Popular Venue",
best_venue,
"Most Matches Hosted"
)

]



for col,item in zip(
[a,b,c],
cards
):

    col.markdown(

    f"""

<div class="card">


<h3 style="color:#38BDF8">

{item[0]}

</h3>


<h2>

{item[1]}

</h2>


<p>

{item[2]}

</p>


</div>

""",

unsafe_allow_html=True

    )





# ==========================
# MODULES
# ==========================


st.divider()

st.markdown(
"## 🚀 Explore Platform"
)



pages=[

("🎯 Match Prediction",
"AI based match outcome prediction",
"pages/1_Match_Prediction.py"),


("🏆 Team Analysis",
"Team comparison and dominance",
"pages/2_Team_Analysis.py"),


("👤 Player Intelligence",
"Batting and bowling analysis",
"pages/3_Player_Statistics.py"),


("🏟 Venue Intelligence",
"Ground and pitch behaviour",
"pages/4_Venue_Analysis.py")

]



for title,desc,page in pages:


    st.markdown(

    f"""

<div class="module">

<h2>

{title}

</h2>

<p>

{desc}

</p>


</div>

""",

unsafe_allow_html=True

    )


    st.page_link(
        page,
        label="Open →"
    )





# ==========================
# FOOTER
# ==========================


st.divider()


if LOGO.exists():

    st.image(
        str(LOGO),
        width=80
    )


st.markdown(

"""

<center style="
color:#94a3b8;
">

IPL InsightXI

<br>

Data Science • Machine Learning • Cricket Analytics

</center>

""",

unsafe_allow_html=True

)   