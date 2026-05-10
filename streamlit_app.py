# 1. PAGE CONFIG & FULL-SCREEN CSS
st.set_page_config(page_title="Biriba", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
        text-align: center; /* Centers standard text and titles */
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Center the scoreboard content */
    .scoreboard {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 15px 5px;
        border-radius: 0px 0px 15px 15px;
        border: 2px solid #4CAF50;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        color: white;
    }

    /* FORCE CENTER ALIGNMENT FOR TABLES */
    [data-testid="stTable"] {
        margin-left: auto;
        margin-right: auto;
    }
    th, td {
        text-align: center !important;
    }
    
    /* Center form elements */
    [data-testid="stForm"] {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ... (Sections 2 through 5 remain the same) ...

# 6. TABLE & RESET
if st.session_state.history:
    st.markdown("### Accumulated Scores")
    # Removing the reverse [::-1] keeps it ascending
    st.table(st.session_state.history)

if st.button("Reset Match", use_container_width=True):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
