import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


from utils.style import load_style



# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="IPL Match Prediction",
    page_icon="🏏",
    layout="wide"
)


load_style()



# ==============================
# PATHS
# ==============================

ROOT = Path(__file__).parent.parent


DATA_PATH = ROOT / "data"
MODEL_PATH = ROOT / "models"
LOGO_PATH = ROOT / "assets" / "team_logos"




# ==============================
# LOAD DATA
# ==============================


@st.cache_data
def load_data():

    matches = pd.read_csv(
        DATA_PATH / "matches.csv"
    )

    return matches



matches = load_data()




# ==============================
# LOAD MODEL
# ==============================


@st.cache_resource
def load_ml_files():

    model = joblib.load(
        MODEL_PATH / "ipl_match_winner_model.pkl"
    )


    feature_columns = joblib.load(
        MODEL_PATH / "feature_columns.pkl"
    )


    return model, feature_columns



model, feature_columns = load_ml_files()




# ==============================
# TEAM LOGOS
# ==============================


TEAM_LOGOS = {


"Mumbai Indians":"MI.png",

"Chennai Super Kings":"CSK.png",

"Royal Challengers Bangalore":"RCB.png",

"Kolkata Knight Riders":"KKR.png",

"Sunrisers Hyderabad":"SRH.png",

"Rajasthan Royals":"RR.png",

"Delhi Capitals":"DC.png",

"Deccan Chargers":"DC_OLD.png",

"Punjab Kings":"PBKS.png",

"Kings XI Punjab":"PBKS.png",

"Gujarat Lions":"GL.png",

"Pune Warriors":"PW.png",

"Rising Pune Supergiants":"RPS.png",

"Kochi Tuskers Kerala":"KTK.png"

}





def show_logo(team):

    file = TEAM_LOGOS.get(team)

    if file:

        path = LOGO_PATH / file

        if path.exists():

            st.image(
                str(path),
                width=140
            )

            return


    st.write("🏏")




# ==============================
# SUPPORTED TEAMS
# ==============================


teams = [

"Mumbai Indians",

"Chennai Super Kings",

"Royal Challengers Bangalore",

"Kolkata Knight Riders",

"Sunrisers Hyderabad",

"Rajasthan Royals",

"Delhi Capitals",

"Deccan Chargers",

"Punjab Kings",

"Kings XI Punjab",

"Gujarat Lions",

"Pune Warriors",

"Rising Pune Supergiants",

"Kochi Tuskers Kerala"

]



# ==============================
# HEADER
# ==============================


st.markdown(

"""
<div class="hero">


<h1 style="color:white;font-size:55px">

🏏 IPL Match Prediction

</h1>


<h2 style="color:#38BDF8">

Machine Learning Powered Prediction

</h2>


<p style="color:#cbd5e1">

Predict IPL match outcomes using historical IPL data
and Random Forest intelligence.

</p>


</div>

""",

unsafe_allow_html=True

)


st.write("")

# ==============================
# MATCH SELECTION
# ==============================


st.markdown(
    "## 🏆 Select Teams"
)



c1,c2,c3 = st.columns([3,1,3])



with c1:

    team1 = st.selectbox(
        "Team 1",
        teams,
        index=0
    )



with c3:

    team2 = st.selectbox(
        "Team 2",
        teams,
        index=1
    )



with c2:

    st.markdown(
        """

<h1 style="
text-align:center;
padding-top:30px;
color:#38BDF8;
">

VS

</h1>

        """,
        unsafe_allow_html=True
    )



if team1 == team2:

    st.warning(
        "Please select different teams"
    )




# ==============================
# LOGO DISPLAY
# ==============================


l1,l2,l3 = st.columns([2,1,2])


with l1:

    show_logo(team1)

    st.markdown(
        f"""
<h3 style="text-align:center">

{team1}

</h3>
""",
        unsafe_allow_html=True
    )



with l2:

    st.markdown(
        """

<h1 style="
padding-top:50px;
text-align:center;
">

⚔️

</h1>

""",
        unsafe_allow_html=True
    )



with l3:

    show_logo(team2)

    st.markdown(
        f"""
<h3 style="text-align:center">

{team2}

</h3>
""",
        unsafe_allow_html=True
    )





# ==============================
# MATCH CONDITIONS
# ==============================


st.divider()


st.markdown(
    "## 🏟 Match Conditions"
)



a,b,c = st.columns(3)



with a:

    season = st.selectbox(
        "Season",
        sorted(
            matches.season.unique(),
            reverse=True
        )
    )



with b:

    venue = st.selectbox(
        "Venue",
        sorted(
            matches.venue.dropna().unique()
        )
    )



with c:

    toss_decision = st.selectbox(
        "Toss Decision",
        [
            "bat",
            "field"
        ]
    )



toss_winner = st.selectbox(
    "Toss Winner",
    [
        team1,
        team2
    ]
)




# ==============================
# FEATURE CREATION
# ==============================


def create_features():


    data = pd.DataFrame(

        0,

        index=[0],

        columns=feature_columns

    )



    # season

    if "season" in data.columns:

        data["season"] = season



    # team 1

    team1_col = f"team1_{team1}"

    if team1_col in data.columns:

        data[team1_col] = 1




    # team 2

    team2_col = f"team2_{team2}"

    if team2_col in data.columns:

        data[team2_col] = 1




    # toss winner

    toss_col = f"toss_winner_{toss_winner}"

    if toss_col in data.columns:

        data[toss_col] = 1




    # toss decision

    if toss_decision == "field":

        if "toss_decision_field" in data.columns:

            data["toss_decision_field"] = 1




    # venue

    venue_col = f"venue_{venue}"

    if venue_col in data.columns:

        data[venue_col] = 1



    return data



input_features = create_features()

# ==============================
# HEAD TO HEAD ANALYSIS
# ==============================


st.divider()


st.markdown(
    "## ⚔️ Head To Head Analysis"
)



# filter previous matches

h2h = matches[

    (

    ((matches["team1"] == team1) &
     (matches["team2"] == team2))

    |

    ((matches["team1"] == team2) &
     (matches["team2"] == team1))

    )

]



total_matches = len(h2h)



team1_wins = len(

    h2h[
        h2h["winner"] == team1
    ]

)



team2_wins = len(

    h2h[
        h2h["winner"] == team2
    ]

)



draws = total_matches - team1_wins - team2_wins




# Display cards


h1,h2,h3 = st.columns(3)



with h1:

    st.metric(

        "Matches Played",

        total_matches

    )



with h2:

    st.metric(

        f"{team1} Wins",

        team1_wins

    )



with h3:

    st.metric(

        f"{team2} Wins",

        team2_wins

    )



if total_matches > 0:


    if team1_wins > team2_wins:

        h2h_message = (

        f"{team1} has historically dominated "
        f"{team2} in previous IPL meetings."

        )


    elif team2_wins > team1_wins:

        h2h_message = (

        f"{team2} has historically dominated "
        f"{team1} in previous IPL meetings."

        )


    else:

        h2h_message = (

        "Both teams have an equal head-to-head record."

        )


    st.info(
        h2h_message
    )


else:

    st.info(
        "No previous IPL meetings available between these teams."
    )

# ==============================
# RECENT FORM ANALYSIS
# ==============================


st.divider()


st.markdown(
    "## 📈 Recent Team Form"
)



def get_recent_form(team):


    team_matches = matches[

        (matches["team1"] == team)
        |
        (matches["team2"] == team)

    ].copy()



    # sort latest first

    team_matches = team_matches.sort_values(

        by="date",

        ascending=False

    )



    recent = team_matches.head(5)



    form = []

    wins = 0
    losses = 0



    for _, row in recent.iterrows():


        if row["winner"] == team:

            form.append("🟢")

            wins += 1


        else:

            form.append("🔴")

            losses += 1



    return {

        "form": form,

        "wins": wins,

        "losses": losses,

        "matches": len(recent)

    }





team1_form = get_recent_form(team1)

team2_form = get_recent_form(team2)





# Display


f1,f2 = st.columns(2)




with f1:


    st.markdown(

    f"""

### {team1}


Recent Form


{" ".join(team1_form["form"])}


Wins:
{team1_form["wins"]}


Losses:
{team1_form["losses"]}

    """

    )





with f2:


    st.markdown(

    f"""

### {team2}


Recent Form


{" ".join(team2_form["form"])}


Wins:
{team2_form["wins"]}


Losses:
{team2_form["losses"]}

    """

    )





# AI observation


if team1_form["wins"] > team2_form["wins"]:


    st.info(

        f"{team1} enters this match with better recent momentum."

    )


elif team2_form["wins"] > team1_form["wins"]:


    st.info(

        f"{team2} enters this match with better recent momentum."

    )


else:


    st.info(

        "Both teams have similar recent form."

    )
    
    # ==============================
# VENUE INTELLIGENCE
# ==============================


st.divider()


st.markdown(
    "## 🏟 Venue Intelligence"
)



def venue_analysis(selected_venue):


    venue_matches = matches[

        matches["venue"] == selected_venue

    ].copy()



    total = len(venue_matches)



    if total == 0:

        return None




    # Batting first wins

    bat_first_wins = venue_matches[

        venue_matches["win_by_runs"] > 0

    ].shape[0]



    chase_wins = venue_matches[

        venue_matches["win_by_wickets"] > 0

    ].shape[0]




    bat_first_percentage = round(

        (bat_first_wins / total) * 100,

        1

    )




    chase_percentage = round(

        (chase_wins / total) * 100,

        1

    )



    return {


        "matches": total,


        "bat_first": bat_first_percentage,


        "chase": chase_percentage


    }





venue_data = venue_analysis(
    venue
)





if venue_data:



    v1,v2,v3 = st.columns(3)



    with v1:

        st.metric(

            "Matches Played",

            venue_data["matches"]

        )



    with v2:

        st.metric(

            "Bat First Win",

            f"{venue_data['bat_first']}%"

        )



    with v3:

        st.metric(

            "Chasing Win",

            f"{venue_data['chase']}%"

        )




    # Venue insight


    if venue_data["chase"] > venue_data["bat_first"]:


        venue_message = (

            f"{venue} generally supports chasing teams."

        )


    elif venue_data["bat_first"] > venue_data["chase"]:


        venue_message = (

            f"{venue} historically favors teams batting first."

        )


    else:

        venue_message = (

            f"{venue} has a balanced record."

        )



    st.info(
        venue_message
    )


else:


    st.warning(

        "Venue data unavailable."

    )
    
# ==============================
# PREDICTION
# ==============================


st.divider()


st.markdown(
    "## 🔮 AI Prediction"
)



predict = st.button(
    "Predict Match Winner",
    use_container_width=True
)



if predict:


    try:


        # --------------------------
        # MODEL PREDICTION
        # --------------------------


        prediction = model.predict(
            input_features
        )


        winner = prediction[0]



        probabilities = model.predict_proba(
            input_features
        )[0]



        model_classes = model.classes_



        probability_df = pd.DataFrame(

            {

                "Team": model_classes,

                "Probability": probabilities * 100

            }

        )



        team1_prob = probability_df.loc[

            probability_df["Team"] == team1,

            "Probability"

        ].sum()



        team2_prob = probability_df.loc[

            probability_df["Team"] == team2,

            "Probability"

        ].sum()



        confidence = round(

            max(probabilities) * 100,

            2

        )



        # --------------------------
        # WINNER CARD
        # --------------------------


        st.success(
            "Prediction Generated Successfully"
        )



        st.markdown(

        f"""

<div class="card">


<h2 style="
text-align:center;
color:#38BDF8;
">

🏆 Predicted Winner

</h2>



<h1 style="
text-align:center;
">

{winner}

</h1>



<h3 style="
text-align:center;
color:#22c55e;
">

Confidence : {confidence}%

</h3>


</div>


        """,

        unsafe_allow_html=True

        )



        show_logo(winner)




        # --------------------------
        # TEAM PROBABILITY
        # --------------------------


        st.divider()


        st.markdown(

            "## 📊 Team Probability Comparison"

        )



        p1,p2 = st.columns(2)



        with p1:


            st.metric(

                team1,

                f"{team1_prob:.1f}%"

            )



            st.progress(

                int(team1_prob)/100

            )



        with p2:


            st.metric(

                team2,

                f"{team2_prob:.1f}%"

            )



            st.progress(

                int(team2_prob)/100

            )





        # --------------------------
        # MATCH SUMMARY
        # --------------------------


        st.divider()


        st.markdown(
            "## 📋 Match Summary"
        )


        s1,s2,s3,s4 = st.columns(4)



        s1.metric(
            "Team 1",
            team1
        )


        s2.metric(
            "Team 2",
            team2
        )


        s3.metric(
            "Venue",
            venue
        )


        s4.metric(
            "Season",
            season
        )





        # --------------------------
        # AI INSIGHT
        # --------------------------


        st.divider()


        st.markdown(
            "## 🧠 Prediction Insight"
        )



        if winner == team1:


            message = (

            f"{team1} has a higher predicted probability "
            f"against {team2} based on historical IPL patterns."
            
            )


        elif winner == team2:


            message = (

            f"{team2} has a higher predicted probability "
            f"against {team1} based on historical IPL patterns."

            )


        else:


            message = (

            f"The model predicts {winner} as the most likely winner."

            )



        st.info(
            message
        )



    except Exception as e:


        st.error(
            "Prediction failed"
        )


        st.exception(e)
