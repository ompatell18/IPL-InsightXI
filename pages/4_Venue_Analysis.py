import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utils.style import load_style


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Venue Intelligence | IPL InsightXI",
    page_icon="🏟️",
    layout="wide"
)


load_style()


ROOT = Path(__file__).parent.parent



# =====================================
# CUSTOM STYLE
# =====================================

st.markdown(
"""
<style>

.stApp{

background:
linear-gradient(
135deg,
#020617,
#111827
);

}


.title{

font-size:45px;
font-weight:900;
color:white;

}


.card{

background:
linear-gradient(
135deg,
#0f172a,
#1e293b
);

padding:25px;

border-radius:20px;

border:1px solid rgba(255,255,255,0.15);

}


</style>
""",
unsafe_allow_html=True
)



# =====================================
# HEADER
# =====================================

st.markdown(

"""
<div class="title">
🏟 IPL Venue Intelligence
</div>

<p style="color:#38BDF8;font-size:20px;">
Advanced Stadium Analytics & Pitch Behaviour
</p>

""",

unsafe_allow_html=True

)




# =====================================
# LOAD DATA
# =====================================


@st.cache_data
def load_matches():

    return pd.read_csv(
        ROOT / "data" / "matches.csv"
    )


@st.cache_data
def load_deliveries():

    return pd.read_csv(
        ROOT / "data" / "deliveries.csv"
    )



matches = load_matches()

deliveries = load_deliveries()




# =====================================
# AUTO COLUMN DETECTION
# =====================================


# Batter column

if "batter" in deliveries.columns:

    batter_column = "batter"

else:

    batter_column = "batsman"



# Runs column

if "batsman_runs" in deliveries.columns:

    runs_column = "batsman_runs"

else:

    runs_column = "batter_runs"



# Bowler column

if "bowler" in deliveries.columns:

    bowler_column = "bowler"

else:

    bowler_column = "bowling_player"



# =====================================
# VENUE SELECTION
# =====================================


venues = sorted(

matches["venue"]

.dropna()

.unique()

)



venue = st.selectbox(

"🏟 Select Stadium",

venues

)



# =====================================
# FILTER DATA
# =====================================


venue_matches = matches[

matches["venue"] == venue

].copy()



venue_delivery = deliveries.merge(

venue_matches[["id"]],

left_on="match_id",

right_on="id",

how="inner"

)



# =====================================
# SCORE ANALYSIS
# =====================================


innings_score = (

venue_delivery

.groupby(

[
"match_id",
"inning"

]

)

["total_runs"]

.sum()

.reset_index()

)



average_score = round(

innings_score["total_runs"].mean(),

2

)



highest_score = int(

innings_score["total_runs"].max()

)



lowest_score = int(

innings_score["total_runs"].min()

)




# =====================================
# VENUE PROFILE
# =====================================


st.markdown(

f"""

<div class="card">

<h1>

{venue}

</h1>


<p>

IPL Venue Performance Report

</p>


</div>

""",

unsafe_allow_html=True

)




st.divider()



# =====================================
# OVERVIEW
# =====================================


st.subheader(

"📊 Venue Overview"

)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

"Matches Hosted",

len(venue_matches)

)



c2.metric(

"Average Score",

average_score

)



c3.metric(

"Highest Score",

highest_score

)



c4.metric(

"Lowest Score",

lowest_score

)





# =====================================
# PITCH RATING
# =====================================


if average_score >= 180:

    pitch_type = "🔥 Batting Paradise"

    pitch_score = 85


elif average_score >= 150:

    pitch_type = "⚖ Balanced Pitch"

    pitch_score = 60


else:

    pitch_type = "🎯 Bowling Friendly"

    pitch_score = 35




st.divider()


st.subheader(

"🏏 Pitch Intelligence"

)



c1,c2 = st.columns(2)



c1.metric(

"Pitch Nature",

pitch_type

)



c2.metric(

"Difficulty Score",

f"{pitch_score}/100"

)




# =====================================
# SCORE DISTRIBUTION
# =====================================


st.subheader(

"📈 Scoring Behaviour"

)



fig = px.histogram(

innings_score,

x="total_runs",

nbins=20,

template="plotly_dark",

title="Runs Distribution At Venue"

)



st.plotly_chart(

fig,

use_container_width=True

)

# =====================================
# TOSS IMPACT ANALYSIS
# =====================================

st.divider()

st.subheader(
"🪙 Toss Advantage Analysis"
)


toss_data = venue_matches.copy()


toss_data["Toss Result"] = (

toss_data["toss_winner"]

==
toss_data["winner"]

)



toss_wins = int(

toss_data["Toss Result"].sum()

)


toss_losses = int(

len(toss_data)-toss_wins

)


toss_percentage = round(

(toss_wins / len(toss_data))*100,

2

)



c1,c2 = st.columns(2)


c1.metric(

"Toss Winner Won Match",

f"{toss_percentage}%"

)


c2.metric(

"Total Matches",

len(toss_data)

)



toss_chart = pd.DataFrame(

{

"Outcome":

[

"Toss Winner Won",

"Toss Winner Lost"

],


"Matches":

[

toss_wins,

toss_losses

]

}

)



fig = px.pie(

toss_chart,

names="Outcome",

values="Matches",

hole=0.5,

template="plotly_dark",

title="Toss Influence"

)



st.plotly_chart(

fig,

use_container_width=True

)





# =====================================
# BATTING FIRST VS CHASING
# =====================================


st.divider()

st.subheader(

"🏏 Batting First vs Chasing"

)



def result_type(row):

    if row["win_by_runs"] > 0:

        return "Batting First Win"

    else:

        return "Chasing Win"




venue_matches["Result Type"] = venue_matches.apply(

result_type,

axis=1

)



result_df = (

venue_matches["Result Type"]

.value_counts()

.reset_index()

)



result_df.columns=[

"Result",

"Matches"

]



fig = px.bar(

result_df,

x="Result",

y="Matches",

text="Matches",

template="plotly_dark",

title="Winning Pattern"

)



st.plotly_chart(

fig,

use_container_width=True

)





# =====================================
# POWERPLAY ANALYSIS
# =====================================


st.divider()

st.subheader(

"⚡ Powerplay Performance (Overs 1-6)"

)



powerplay = venue_delivery[

venue_delivery["over"] <= 6

]



pp_score = (

powerplay

.groupby("match_id")

["total_runs"]

.sum()

.reset_index()

)



avg_pp = round(

pp_score["total_runs"].mean(),

2

)



max_pp = int(

pp_score["total_runs"].max()

)



c1,c2 = st.columns(2)



c1.metric(

"Average Powerplay Runs",

avg_pp

)


c2.metric(

"Highest Powerplay",

max_pp

)



fig = px.histogram(

pp_score,

x="total_runs",

nbins=15,

template="plotly_dark",

title="Powerplay Score Distribution"

)



st.plotly_chart(

fig,

use_container_width=True

)






# =====================================
# DEATH OVERS ANALYSIS
# =====================================


st.divider()


st.subheader(

"🔥 Death Overs Performance (16-20)"

)



death = venue_delivery[

venue_delivery["over"] >= 16

]



death_score=(

death

.groupby("match_id")

["total_runs"]

.sum()

.reset_index()

)



avg_death = round(

death_score["total_runs"].mean(),

2

)



max_death = int(

death_score["total_runs"].max()

)



c1,c2 = st.columns(2)



c1.metric(

"Average Death Runs",

avg_death

)


c2.metric(

"Highest Death Score",

max_death

)



fig = px.bar(

death_score,

x="match_id",

y="total_runs",

template="plotly_dark",

title="Death Overs Scoring"

)



st.plotly_chart(

fig,

use_container_width=True

)





# =====================================
# BOUNDARY ANALYSIS
# =====================================


st.divider()


st.subheader(

"💥 Boundary Analysis"

)



total_fours = int(

(

venue_delivery[runs_column]==4

)

.sum()

)



total_sixes = int(

(

venue_delivery[runs_column]==6

)

.sum()

)



avg_sixes = round(

total_sixes /

len(venue_matches),

2

)



avg_fours = round(

total_fours /

len(venue_matches),

2

)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

"Total Fours",

total_fours

)


c2.metric(

"Total Sixes",

total_sixes

)


c3.metric(

"Sixes / Match",

avg_sixes

)


c4.metric(

"Fours / Match",

avg_fours

)



boundary_df = pd.DataFrame(

{

"Boundary":

[

"Fours",

"Sixes"

],


"Count":

[

total_fours,

total_sixes

]

}

)



fig = px.pie(

boundary_df,

names="Boundary",

values="Count",

hole=0.5,

template="plotly_dark",

title="Boundary Distribution"

)



st.plotly_chart(

fig,

use_container_width=True

)

# =====================================
# TOP BATTERS AT VENUE
# =====================================


st.divider()

st.header(
"🏏 Best Batters At This Venue"
)



top_batters = (

venue_delivery

.groupby(batter_column)[runs_column]

.sum()

.sort_values(

ascending=False

)

.head(10)

.reset_index()

)



top_batters.columns = [

"Player",

"Runs"

]



st.dataframe(

top_batters,

hide_index=True,

use_container_width=True

)



fig = px.bar(

top_batters,

x="Runs",

y="Player",

orientation="h",

template="plotly_dark",

title="Highest Run Scorers At Venue"

)


st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# TOP BOWLERS AT VENUE
# =====================================


st.divider()


st.header(

"🎯 Best Bowlers At This Venue"

)



if "player_dismissed" in venue_delivery.columns:


    wickets_data = venue_delivery[

        venue_delivery["player_dismissed"].notna()

    ]


    top_bowlers = (

        wickets_data

        .groupby(bowler_column)

        .size()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )


    top_bowlers.columns=[

        "Bowler",

        "Wickets"

    ]



    st.dataframe(

        top_bowlers,

        hide_index=True,

        use_container_width=True

    )



    fig = px.bar(

        top_bowlers,

        x="Wickets",

        y="Bowler",

        orientation="h",

        template="plotly_dark",

        title="Most Wickets At Venue"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )





# =====================================
# TEAM PERFORMANCE
# =====================================


st.divider()


st.header(

"🏆 Most Successful Teams At Venue"

)



team_wins = (

venue_matches["winner"]

.value_counts()

.reset_index()

)



team_wins.columns=[

"Team",

"Wins"

]



st.dataframe(

team_wins,

hide_index=True,

use_container_width=True

)



fig = px.bar(

team_wins.head(10),

x="Wins",

y="Team",

orientation="h",

template="plotly_dark",

title="Team Wins At Stadium"

)



st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# TEAM VENUE EXPLORER
# =====================================


st.divider()


st.header(

"🔍 Team Performance At This Venue"

)



available_teams = sorted(

list(

set(venue_matches.team1)

.union(

set(venue_matches.team2)

)

)

)



selected_team = st.selectbox(

"Select Team",

available_teams

)



team_matches = venue_matches[

(

venue_matches.team1 == selected_team

)

|

(

venue_matches.team2 == selected_team

)

]



wins = (

team_matches.winner == selected_team

).sum()



win_percentage = round(

(wins /

len(team_matches))

*

100,

2

) if len(team_matches)>0 else 0




c1,c2,c3 = st.columns(3)



c1.metric(

"Matches",

len(team_matches)

)


c2.metric(

"Wins",

wins

)


c3.metric(

"Win %",

f"{win_percentage}%"

)




# =====================================
# VENUE COMPARISON
# =====================================


st.divider()


st.header(

"⚔ Compare Two Venues"

)



venue_compare = st.selectbox(

"Select Second Venue",

venues,

index=0

)



comparison=[]



for v in [venue,venue_compare]:


    temp_matches = matches[

        matches.venue == v

    ]


    temp_delivery = deliveries.merge(

        temp_matches[["id"]],

        left_on="match_id",

        right_on="id",

        how="inner"

    )


    score = (

        temp_delivery

        .groupby(

        ["match_id","inning"]

        )[

        "total_runs"

        ]

        .sum()

        .mean()

    )


    comparison.append(

        {

        "Venue":v,

        "Matches":len(temp_matches),

        "Average Score":round(score,2)

        }

    )



comparison_df = pd.DataFrame(

comparison

)



st.dataframe(

comparison_df,

hide_index=True,

use_container_width=True

)



fig = px.bar(

comparison_df,

x="Venue",

y="Average Score",

template="plotly_dark",

title="Venue Scoring Comparison"

)



st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# AI VENUE REPORT
# =====================================


st.divider()


st.header(

"🤖 Venue Intelligence Report"

)



if average_score >=180:

    pitch_text = (

    "A high scoring batting friendly venue."

    )

elif average_score >=150:

    pitch_text = (

    "A balanced venue where both skills matter."

    )

else:

    pitch_text = (

    "A challenging bowling friendly venue."

    )




if toss_percentage >=55:

    toss_text = (

    "Toss has a strong influence here."

    )

else:

    toss_text = (

    "Toss advantage is limited."

    )




best_team = (

team_wins.iloc[0]["Team"]

if len(team_wins)>0

else "Not Available"

)




st.markdown(

f"""

<div class="card">


<h3>

{venue}

</h3>


<p>

🏏 Pitch:

{pitch_text}

</p>


<p>

🪙 Toss:

{toss_text}

</p>


<p>

🏆 Most successful team:

{best_team}

</p>


<p>

📊 Average scoring:

{average_score} runs

</p>


</div>


""",

unsafe_allow_html=True

)



st.caption(

"IPL InsightXI | Venue Intelligence Platform"

)   