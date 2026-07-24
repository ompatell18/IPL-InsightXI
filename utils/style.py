import streamlit as st


def load_style():

    st.markdown(
        """
        <style>

        .stApp {
            background: linear-gradient(
                135deg,
                #020617,
                #111827
            );
        }


        section[data-testid="stSidebar"] {

            background:#020617;

        }


        header {

            visibility:hidden;

        }


        .hero {

            background:#111827;

            padding:50px;

            border-radius:25px;

            border:1px solid rgba(255,255,255,0.15);

        }


        .hero-title {

            color:white;

            font-size:60px;

            font-weight:900;

        }


        .hero-sub {

            color:#38BDF8;

            font-size:22px;

        }


        .card {

            background:#111827;

            padding:25px;

            border-radius:20px;

            border:1px solid rgba(255,255,255,0.15);

        }


        .card h1 {

            color:#38BDF8;

            font-size:40px;

        }


        .card h2 {

            color:white;

        }


        .card p {

            color:#cbd5e1;

        }


        .module {

            background:#111827;

            padding:25px;

            border-radius:20px;

            border:1px solid rgba(255,255,255,0.15);

        }


        .module h2 {

            color:#38BDF8;

        }


        .module p {

            color:#cbd5e1;

        }


        </style>

        """,

        unsafe_allow_html=True
    )