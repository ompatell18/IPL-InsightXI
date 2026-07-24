import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


from utils.style import load_style



# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Player Intelligence | IPL InsightXI",

    page_icon="👤",

    layout="wide"

)


load_style()


ROOT = Path(__file__).parent.parent



# =====================================
# PREMIUM UI
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


.subtitle{

font-size:20px;
color:#38BDF8;

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

border:

1px solid rgba(255,255,255,0.15);

}


.metric-card{

background:
rgba(255,255,255,0.08);

padding:20px;

border-radius:15px;

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

👤 IPL Player Intelligence

</div>


<div class="subtitle">

Complete Cricket Performance Analytics

</div>


""",

unsafe_allow_html=True

)


st.write("")



# =====================================
# LOAD DATA
# =====================================


@st.cache_data
def load_matches():

    return pd.read_csv(

        ROOT /
        "data" /
        "matches.csv"

    )



@st.cache_data
def load_deliveries():

    return pd.read_csv(

        ROOT /
        "data" /
        "deliveries.csv"

    )



matches = load_matches()

deliveries = load_deliveries()




# =====================================
# ADD SEASON TO DELIVERY DATA
# =====================================


if "season" not in deliveries.columns:


    deliveries = deliveries.merge(

        matches[

            [

            "id",

            "season"

            ]

        ],

        left_on="match_id",

        right_on="id",

        how="left"

    )




# =====================================
# HANDLE COLUMN DIFFERENCE
# =====================================


if "batter" in deliveries.columns:

    batter_column = "batter"


else:

    batter_column = "batsman"




# =====================================
# PLAYER LIST
# =====================================


players = sorted(

    deliveries[batter_column]

    .dropna()

    .unique()

)




# =====================================
# PLAYER SEARCH
# =====================================


st.divider()


st.subheader(
"🔎 Search Player"
)



player = st.selectbox(

    "Select Player",

    players

)




# =====================================
# FILTER PLAYER DATA
# =====================================


batting_data = deliveries[

    deliveries[batter_column]==player

]



bowling_data = deliveries[

    deliveries.bowler==player

]





# =====================================
# PLAYER CAREER CALCULATION
# =====================================


matches_played = (

batting_data

.match_id

.nunique()

)



runs = (

batting_data

.batsman_runs

.sum()

)



balls = len(

batting_data

)



strike_rate = round(

(runs/balls)*100,

2

) if balls else 0




innings = (

batting_data

.groupby("match_id")

.size()

.count()

)



average = round(

runs/innings,

2

) if innings else 0




highest_score = (

batting_data

.groupby("match_id")

.batsman_runs

.sum()

.max()

)



fours = (

batting_data

.batsman_runs

.eq(4)

.sum()

)



sixes = (

batting_data

.batsman_runs

.eq(6)

.sum()

)




# =====================================
# BOWLING CALCULATION
# =====================================


wickets = (

bowling_data

[

bowling_data.player_dismissed.notna()

]

.shape[0]

)



runs_conceded = (

bowling_data

.total_runs

.sum()

)



balls_bowled = len(

bowling_data

)



economy = round(

runs_conceded /

( balls_bowled / 6 ),

2

) if balls_bowled else 0




# =====================================
# PLAYER PROFILE
# =====================================


st.markdown(

f"""

<div class="card">


<h1>

{player}

</h1>


<p>

IPL Career Performance Profile

</p>


</div>

""",

unsafe_allow_html=True

)



st.divider()




# =====================================
# BATTING SECTION
# =====================================


st.header(
"🏏 Batting Performance"
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

"Runs",

int(runs)

)


c2.metric(

"Matches",

matches_played

)


c3.metric(

"Average",

average

)


c4.metric(

"Strike Rate",

strike_rate

)




c1,c2,c3,c4 = st.columns(4)



c1.metric(

"Highest Score",

int(highest_score)

)


c2.metric(

"Fours",

fours

)


c3.metric(

"Sixes",

sixes

)


c4.metric(

"Innings",

innings

)




# =====================================
# BOWLING SECTION
# =====================================


st.divider()


st.header(

"🎯 Bowling Performance"

)



c1,c2,c3 = st.columns(3)



c1.metric(

"Wickets",

wickets

)


c2.metric(

"Economy",

economy

)


c3.metric(

"Runs Conceded",

int(runs_conceded)

)



# =====================================
# BASIC INSIGHT
# =====================================


st.divider()


st.subheader(

"📌 Player Snapshot"

)



if runs > 3000:


    insight = "Elite IPL run scorer with long-term consistency."


elif runs > 1000:


    insight = "Strong IPL performer with valuable contributions."


else:

    insight = "Developing IPL career profile."




st.markdown(

f"""

<div class="card">


<h3>

{player}

</h3>


<p>

{insight}

</p>


</div>

""",

unsafe_allow_html=True

)



st.caption(

"IPL InsightXI | Player Analytics"

)

st.caption(
"IPL InsightXI | Player Analytics"
)

# =====================================
# SEASON PERFORMANCE ANALYSIS
# =====================================


st.divider()

st.header(
"📈 Season Performance Analysis"
)



season_batting = (

batting_data

.groupby("season")

.agg(

{

"batsman_runs":"sum",

"match_id":"nunique"

}

)

.reset_index()

)



season_batting.columns=[

"Season",

"Runs",

"Matches"

]



fig = px.line(

season_batting,

x="Season",

y="Runs",

markers=True,

template="plotly_dark",

title="Runs Scored Each Season"

)


st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# BOWLING SEASON ANALYSIS
# =====================================


if wickets > 0:


    season_wickets=(


    bowling_data[

    bowling_data.player_dismissed.notna()

    ]

    .groupby("season")

    .size()

    .reset_index()

    )


    season_wickets.columns=[

    "Season",

    "Wickets"

    ]



    fig = px.bar(

        season_wickets,

        x="Season",

        y="Wickets",

        text="Wickets",

        template="plotly_dark",

        title="Wickets By Season"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )




# =====================================
# VENUE PERFORMANCE
# =====================================


st.divider()


st.header(

"🏟 Venue Performance"

)



venue_analysis = batting_data.merge(

matches[

[

"id",

"venue"

]

],

left_on="match_id",

right_on="id",

how="left"

)



venue_stats=(

venue_analysis

.groupby("venue")

.batsman_runs

.agg(

[

"sum",

"mean"

]

)

.sort_values(

by="sum",

ascending=False

)

.head(10)

.reset_index()

)



venue_stats.columns=[

"Venue",

"Total Runs",

"Average Runs"

]



st.dataframe(

venue_stats,

use_container_width=True,

hide_index=True

)




fig = px.bar(

venue_stats,

x="Total Runs",

y="Venue",

orientation="h",

template="plotly_dark",

title="Best Venues For Player"

)


st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# OPPONENT ANALYSIS
# =====================================


st.divider()


st.header(

"⚔ Performance Against Teams"

)



opponent_data = batting_data.merge(

matches[

[

"id",

"team1",

"team2"

]

],

left_on="match_id",

right_on="id",

how="left"

)



def find_opponent(row):


    if row.team1 == row.batting_team:

        return row.team2

    else:

        return row.team1




opponent_data["Opponent"] = opponent_data.apply(

find_opponent,

axis=1

)




opponent_stats=(

opponent_data

.groupby("Opponent")

.batsman_runs

.sum()

.sort_values(

ascending=False

)

.reset_index()

)



opponent_stats.columns=[

"Opponent",

"Runs"

]



st.dataframe(

opponent_stats,

use_container_width=True,

hide_index=True

)



fig = px.bar(

opponent_stats,

x="Runs",

y="Opponent",

orientation="h",

template="plotly_dark",

title="Runs Against Teams"

)


st.plotly_chart(

fig,

use_container_width=True

)





# =====================================
# MATCH PHASE ANALYSIS
# =====================================


st.divider()


st.header(

"⚡ Match Situation Analysis"

)



phase_data = batting_data.copy()



phase_data["ball_number"] = (

phase_data.groupby(

"match_id"

).cumcount()+1

)



def phase(ball):

    if ball <= 36:

        return "Powerplay"


    elif ball <= 90:

        return "Middle Overs"


    else:

        return "Death Overs"




phase_data["Phase"] = phase_data.ball_number.apply(

phase

)



phase_stats=(

phase_data

.groupby("Phase")

.batsman_runs

.sum()

.reset_index()

)



fig = px.pie(

phase_stats,

names="Phase",

values="batsman_runs",

hole=0.5,

template="plotly_dark",

title="Runs Distribution By Match Phase"

)


st.plotly_chart(

fig,

use_container_width=True

)





# =====================================
# PLAYER IMPACT SCORE
# =====================================


st.divider()


st.header(

"🔥 Player Impact Rating"

)



impact = (

(runs/6000)*50

+

(wickets/150)*30

+

(strike_rate/200)*20

)



impact = min(

round(impact,2),

100

)



st.markdown(

f"""

<div class="card">


<h1>

🔥 {impact}/100

</h1>


<p>

Overall IPL Impact Rating

</p>


</div>

""",

unsafe_allow_html=True

)

st.caption(
"IPL InsightXI | Player Analytics"
)

# =====================================
# PLAYER COMPARISON
# =====================================


st.divider()

st.header(
"⚔ Player Comparison"
)



compare_players = sorted(players)



col1,col2 = st.columns(2)



with col1:

    player_a = st.selectbox(

        "Select Player A",

        compare_players,

        index=0

    )


with col2:

    player_b = st.selectbox(

        "Select Player B",

        compare_players,

        index=1

    )





def player_stats(name):


    batting = deliveries[

        deliveries[batter_column]==name

    ]


    bowling = deliveries[

        deliveries.bowler==name

    ]


    runs = batting.batsman_runs.sum()


    balls = len(batting)


    sr = round(

        (runs/balls)*100,

        2

    ) if balls else 0



    matches = batting.match_id.nunique()



    wickets = bowling[

        bowling.player_dismissed.notna()

    ].shape[0]



    return {

        "Runs":int(runs),

        "Matches":matches,

        "Strike Rate":sr,

        "Wickets":wickets

    }





stats_a = player_stats(player_a)

stats_b = player_stats(player_b)





comparison = pd.DataFrame(

{

player_a:stats_a,

player_b:stats_b

}

)



st.dataframe(

comparison,

use_container_width=True

)





# =====================================
# RADAR COMPARISON
# =====================================


radar_df = pd.DataFrame(

{

"Metric":[

"Runs",

"Matches",

"Strike Rate",

"Wickets"

],


player_a:[

stats_a["Runs"]/50,

stats_a["Matches"],

stats_a["Strike Rate"],

stats_a["Wickets"]*10

],


player_b:[

stats_b["Runs"]/50,

stats_b["Matches"],

stats_b["Strike Rate"],

stats_b["Wickets"]*10

]

}

)



radar = px.line_polar(

radar_df,

r=player_a,

theta="Metric",

line_close=True,

template="plotly_dark",

title=f"{player_a} Comparison"

)


st.plotly_chart(

radar,

use_container_width=True

)





# =====================================
# IPL PLAYER RANKINGS
# =====================================


st.divider()


st.header(

"🏆 IPL Player Rankings"

)



# -------------------------------------
# TOP RUN SCORERS
# -------------------------------------


st.subheader(

"🔥 Top Run Scorers"

)



run_rank=(

deliveries

.groupby(batter_column)

.batsman_runs

.sum()

.sort_values(

ascending=False

)

.head(15)

.reset_index()

)



run_rank.columns=[

"Player",

"Runs"

]



st.dataframe(

run_rank,

hide_index=True,

use_container_width=True

)



fig = px.bar(

run_rank,

x="Runs",

y="Player",

orientation="h",

template="plotly_dark",

title="Most IPL Runs"

)


st.plotly_chart(

fig,

use_container_width=True

)




# -------------------------------------
# TOP WICKET TAKERS
# -------------------------------------


st.subheader(

"🎯 Top Wicket Takers"

)



wicket_rank=(

deliveries[

deliveries.player_dismissed.notna()

]

.groupby("bowler")

.size()

.sort_values(

ascending=False

)

.head(15)

.reset_index()

)



wicket_rank.columns=[

"Player",

"Wickets"

]



st.dataframe(

wicket_rank,

hide_index=True,

use_container_width=True

)



fig = px.bar(

wicket_rank,

x="Wickets",

y="Player",

orientation="h",

template="plotly_dark",

title="Most IPL Wickets"

)


st.plotly_chart(

fig,

use_container_width=True

)




# -------------------------------------
# STRIKE RATE LEADERS
# -------------------------------------


st.subheader(

"⚡ Highest Strike Rate Players"

)



sr_rank=(

deliveries

.groupby(batter_column)

.agg(

{

"batsman_runs":"sum",

"match_id":"count"

}

)

.reset_index()

)



sr_rank["Strike Rate"]=(

sr_rank.batsman_runs /

sr_rank.match_id

*

100

).round(2)



sr_rank=(

sr_rank

.sort_values(

"Strike Rate",

ascending=False

)

.head(15)

)



sr_rank.columns=[

"Player",

"Runs",

"Balls",

"Strike Rate"

]



st.dataframe(

sr_rank,

hide_index=True,

use_container_width=True

)





# -------------------------------------
# SIX HITTING RANKING
# -------------------------------------


st.subheader(

"💥 Most Six Hitters"

)



six_rank=(

deliveries[

deliveries.batsman_runs==6

]

.groupby(batter_column)

.size()

.sort_values(

ascending=False

)

.head(15)

.reset_index()

)



six_rank.columns=[

"Player",

"Sixes"

]



fig = px.bar(

six_rank,

x="Sixes",

y="Player",

orientation="h",

template="plotly_dark",

title="Maximum Sixes"

)



st.plotly_chart(

fig,

use_container_width=True

)



st.caption(

"IPL InsightXI | Player Analytics Platform"

)