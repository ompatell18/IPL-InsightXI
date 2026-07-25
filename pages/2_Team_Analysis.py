import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os


from utils.style import load_style



# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Team Analysis | IPL InsightXI",

    page_icon="📊",

    layout="wide"

)


load_style()


ROOT = Path(__file__).parent.parent



# =====================================
# UI STYLE
# =====================================


st.markdown(
"""
<style>


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

border:
1px solid rgba(255,255,255,0.15);

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
📊 IPL Team Intelligence
</div>


<p style="color:#38BDF8;font-size:20px;">
Deep performance analysis of IPL franchises
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

        ROOT /
        "data" /
        "matches.csv"

    )



matches = load_matches()



@st.cache_data
def load_deliveries():

    return pd.read_csv(

        ROOT /
        "data" /
        "deliveries.csv"

    )



deliveries = load_deliveries()



# =====================================
# TEAM LOGOS
# =====================================


logo_folder = (

ROOT /
"assets" /
"team_logos"

)



logo_map = {


"Mumbai Indians":
[
"MI.png",
"Mumbai Indians.png"
],


"Chennai Super Kings":
[
"CSK.png",
"Chennai Super Kings.png"
],


"Royal Challengers Bangalore":
[
"RCB.png",
"Royal Challengers Bangalore.png"
],


"Kolkata Knight Riders":
[
"KKR.png"
],


"Sunrisers Hyderabad":
[
"SRH.png"
],


"Rajasthan Royals":
[
"RR.png"
],


"Delhi Capitals":
[
"DC.png"
],


"Delhi Daredevils":
[
"DC.png"
],


"Kings XI Punjab":
[
"PBKS.png"
],


"Punjab Kings":
[
"PBKS.png"
]


}




def get_logo(team):


    files = logo_map.get(

        team,

        []

    )


    for f in files:


        path = logo_folder / f


        if path.exists():

            return str(path)



    return None





# =====================================
# TEAM SELECTION
# =====================================



teams = sorted(

set(matches.team1)

.union(

set(matches.team2)

)

)



team = st.selectbox(

"Select Team",

teams

)



st.divider()



# =====================================
# TEAM PROFILE CARD
# =====================================



col1,col2 = st.columns([1,3])



with col1:


    logo = get_logo(team)


    if logo:

        st.image(

            logo,

            width=170

        )



with col2:


    st.markdown(

f"""

<div class="card">


<h1>
{team}
</h1>


<p>
IPL Franchise Performance Dashboard
</p>


</div>

""",

unsafe_allow_html=True

)




# =====================================
# FILTER DATA
# =====================================


team_matches = matches[

(matches.team1==team)

|

(matches.team2==team)

]



wins = team_matches[

team_matches.winner==team

].shape[0]



losses = (

len(team_matches)

-

wins

)



win_percentage = round(

wins /

len(team_matches)

*

100,

2

)




# =====================================
# KPI CARDS
# =====================================


st.subheader(
"Performance Overview"
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

"Matches",

len(team_matches)

)



c2.metric(

"Wins",

wins

)



c3.metric(

"Losses",

losses

)



c4.metric(

"Win %",

f"{win_percentage}%"

)




st.divider()



# =====================================
# RUN ANALYSIS
# =====================================


team_delivery = deliveries[

(deliveries.batting_team==team)

]



total_runs = team_delivery.total_runs.sum()



wickets = deliveries[

deliveries.player_dismissed.notna()

]


team_wickets = wickets[

wickets.bowling_team==team

].shape[0]




c1,c2 = st.columns(2)



c1.metric(

"Total Runs Scored",

int(total_runs)

)


c2.metric(

"Total Wickets Taken",

team_wickets

)




# =====================================
# WIN LOSS GRAPH
# =====================================


st.subheader(
"Win Loss Distribution"
)



result_df = pd.DataFrame(

{

"Result":

[

"Wins",

"Losses"

],

"Count":

[

wins,

losses

]

}

)



fig = px.pie(

result_df,

names="Result",

values="Count",

hole=.5,

template="plotly_dark"

)



st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# SEASON PERFORMANCE
# =====================================


st.subheader(

"Season Wise Performance"

)



season_data = team_matches.groupby(

"season"

).apply(

lambda x:

pd.Series({

"Wins":

(x.winner==team).sum(),

"Matches":

len(x)

})

).reset_index()



season_data["Win %"] = (

season_data.Wins /

season_data.Matches *

100

).round(1)



fig = px.line(

season_data,

x="season",

y="Win %",

markers=True,

template="plotly_dark",

title="Season Win Percentage"

)



st.plotly_chart(

fig,

use_container_width=True

)




# =====================================
# TOP OPPONENTS
# =====================================


st.subheader(

"Most Played Opponents"

)



opponents=[]


for _,row in team_matches.iterrows():


    if row.team1==team:

        opponents.append(row.team2)

    else:

        opponents.append(row.team1)




opp_df = pd.Series(

opponents

).value_counts().reset_index()



opp_df.columns=[

"Opponent",

"Matches"

]



st.dataframe(

opp_df,

hide_index=True,

use_container_width=True

)




# =====================================
# INSIGHT REPORT
# =====================================


st.subheader(

"AI Team Summary"

)



st.markdown(

f"""

<div class="card">


<h3>{team}</h3>


<p>

Played:
<b>{len(team_matches)}</b>
matches

</p>


<p>

Won:
<b>{wins}</b>
matches

</p>


<p>

Overall Success Rate:
<b>{win_percentage}%</b>

</p>


<p>

Total Runs:
<b>{int(total_runs)}</b>

</p>


</div>

""",

unsafe_allow_html=True

)


    

st.caption(

"IPL InsightXI | Team Analytics Platform"

)