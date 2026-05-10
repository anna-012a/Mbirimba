import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. PAGE CONFIG & FULL-SCREEN MOBILE CSS
st.set_page_config(page_title="Biriba Tracker", layout="centered")

st.markdown("""
    <style>
    /* Remove top margins and force center */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
        text-align: center;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* The Scoreboard Header */
    .scoreboard {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 15px 5px;
        border-radius: 0px 0px 15px 15px;
        border: 2px solid #4CAF50;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        color: white;
    }

    /* Centering the Table and Row Text */
    [data-testid="stTable"] {
        margin-left: auto;
        margin-right: auto;
    }
    th, td {
        text-align: center !important;
    }

    /* Centering Input Labels and Number Text */
    [data-testid="stWidgetLabel"] {
        text-align: center;
        display: block;
        width: 100%;
    }
    input {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE CONNECTION (Google Sheets)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Ensure worksheet name matches your Google Sheet tab exactly
    df = conn.read(worksheet="Sheet1", ttl="0") 
    series_dad = int(df.iloc[0]["Dad"])
    series_mom = int(df.iloc[0]["Mom"])
except Exception:
    # Fallback default if Sheet is not connected yet
    series_dad, series_mom = 20, 6

# 3. TOP HEADER (The 20 vs 6)
st.markdown(f"""
    <div class="scoreboard">
        <div>Dad <span style='color:#4CAF50;'>{series_dad}</span></div>
        <div>vs</div>
        <div><span style='color:#4CAF50;'>{series_mom}</span> Mom</div>
    </div>
    """, unsafe_allow_html=True)

# 4. INITIALIZE SESSION STATE
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None

# 5. ROUND LOGIC & INPUTS
round_num = len(st.session_state.history) + 1

if st.session_state.first_dealer is None:
    st.subheader("Ποιος μοιράζει πρώτος;")
    col_a, col_b = st.columns(2)
    if col_a.button("Μπαμπάς", use_container_width=True):
        st.session_state.first_dealer = "Dad"
        st.rerun()
    if col_b.button("Μαμά", use_container_width=True):
        st.session_state.first_dealer = "Mom"
        st.rerun()
else:
    # Alternate roles automatically
    players = ["Dad", "Mom"] if st.session_state.first_dealer == "Dad" else ["Mom", "Dad"]
    current_dealer = players[0] if round_num % 2 != 0 else players[1]
    
    st.markdown(f"### Γύρος {round_num}")
    st.markdown(f"🃏 **{current_dealer}** μοιράζει")

    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        # placeholder="" hides the "Press Enter" message
        d_pts = f1.number_input("Dad", step=5, value=0, placeholder="")
        m_pts = f2.number_input("Mom", step=5, value=0, placeholder="")
        
        if f3.form_submit_button("OK", use_container_width=True):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({
                "Rd": round_num,
                "Dad Total": st.session_state.scores["Dad"], 
                "Mom Total": st.session_state.scores["Mom"]
            })
            st.rerun()

# 6. TABLE (Ascending) & RESET
if st.session_state.history:
    st.markdown("---")
    st.table(st.session_state.history)

if st.button("Reset Current Match", use_container_width=True):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
