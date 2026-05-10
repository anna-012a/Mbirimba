import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. PAGE CONFIG
st.set_page_config(page_title="Biriba Tracker", layout="centered")

WINNING_SCORE = 3510

# 2. CSS FOR MOBILE & UI
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
        text-align: center;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
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

    [data-testid="stTable"] {
        margin-left: auto;
        margin-right: auto;
    }
    th, td {
        text-align: center !important;
    }

    [data-testid="stWidgetLabel"] {
        text-align: center;
        display: block;
        width: 100%;
    }
    
    input {
        text-align: center;
    }
    /* Hide the "Press Enter" instruction */
    input::placeholder { color: transparent !important; }
    input::-webkit-input-placeholder { color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATABASE CONNECTION
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Read the first row of the sheet
    df = conn.read(worksheet="Sheet1", ttl="0") 
    series_dad = int(df.iloc[0]["Dad"])
    series_mom = int(df.iloc[0]["Mom"])
except Exception:
    # Fallback values if sheet is unreachable
    series_dad, series_mom = 20, 6

# 4. HEADER (THE SERIES SCORE)
st.markdown(f"""
    <div class="scoreboard">
        <div>Dad <span style='color:#4CAF50;'>{series_dad}</span></div>
        <div>vs</div>
        <div><span style='color:#4CAF50;'>{series_mom}</span> Mom</div>
    </div>
    """, unsafe_allow_html=True)

# 5. INITIALIZE MATCH STATE
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None

# 6. WINNER LOGIC & DATABASE WRITE
dad_total = st.session_state.scores["Dad"]
mom_total = st.session_state.scores["Mom"]

if dad_total >= WINNING_SCORE or mom_total >= WINNING_SCORE:
    winner_name = "Dad" if dad_total > mom_total else "Mom"
    
    if winner_name == "Dad":
        st.balloons()
        st.success(f"🏆 Νικητής ο Μπαμπάς με {dad_total}!")
    else:
        st.balloons()
        st.success(f"🏆 Νικήτρια η Μαμά με {mom_total}!")
    
    if st.button(f"Καταγραφή Νίκης για {winner_name}", use_container_width=True):
        try:
            # Prepare new data
            new_dad = series_dad + 1 if winner_name == "Dad" else series_dad
            new_mom = series_mom + 1 if winner_name == "Mom" else series_mom
            update_df = pd.DataFrame([{"Dad": new_dad, "Mom": new_mom}])
            
            # Write to Google Sheets
            conn.update(worksheet="Sheet1", data=update_df)
            
            # Reset Match for next time
            st.session_state.scores = {"Dad": 0, "Mom": 0}
            st.session_state.history = []
            st.session_state.first_dealer = None
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# 7. ROUND INPUTS
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
    players = ["Dad", "Mom"] if st.session_state.first_dealer == "Dad" else ["Mom", "Dad"]
    current_dealer = players[0] if round_num % 2 != 0 else players[1]
    
    st.markdown(f"### Γύρος {round_num}")
    st.markdown(f"🃏 **{current_dealer}** μοιράζει")

    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        d_pts = f1.number_input("Dad", step=5, value=0)
        m_pts = f2.number_input("Mom", step=5, value=0)
        
        if f3.form_submit_button("OK", use_container_width=True):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({
                "Rd": round_num,
                "Dad Total": st.session_state.scores["Dad"], 
                "Mom Total": st.session_state.scores["Mom"]
            })
            st.rerun()

# 8. HISTORY TABLE & RESET
if st.session_state.history:
    st.table(st.session_state.history)

if st.button("Reset Match (No Save)", use_container_width=True):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
