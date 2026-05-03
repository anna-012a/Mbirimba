import streamlit as st

# Force a clean mobile layout
st.set_page_config(page_title="Biriba", layout="centered")

# Corrected CSS to reduce padding and keep it on one screen
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
    /* Tighten the table rows */
    [data-testid="stTable"] td {padding: 5px !important;}
    </style>
    """, unsafe_allow_html=True)

# Initialize State
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.series = {"Dad": 20, "Mom": 6}
    st.session_state.first_dealer = None

WINNING_SCORE = 3510

# 1. TOP HEADER: Overall Series Score
c1, c2 = st.columns(2)
c1.metric("Dad Series", st.session_state.series["Dad"])
c2.metric("Mom Series", st.session_state.series["Mom"])

st.divider()

# 2. DEALER SELECTION / ROLE DISPLAY
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
    current_mbiribakia = players[1] if round_num % 2 != 0 else players[0]
    
    st.write(f"**Γύρος {round_num}** | 🃏 **{current_dealer}** μοιράζει")

    # 3. SCORE INPUT
    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        d_pts = f1.number_input("Dad", step=5, value=0)
        m_pts = f2.number_input("Mom", step=5, value=0)
        if f3.form_submit_button("OK"):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({
                "Rd": round_num,
                "Dad Total": st.session_state.scores["Dad"], 
                "Mom Total": st.session_state.scores["Mom"]
            })
            st.rerun()

# 4. WINNER CHECK & TABLE
dad_total = st.session_state.scores["Dad"]
mom_total = st.session_state.scores["Mom"]

if dad_total >= WINNING_SCORE or mom_total >= WINNING_SCORE:
    if dad_total > mom_total:
        st.warning(f"🏆 Νικητής ο Μπαμπάς: {dad_total}!")
        if st.button("Record Win & Reset"):
            st.session_state.series["Dad"] += 1
            st.session_state.scores = {"Dad": 0, "Mom": 0}
            st.session_state.history = []
            st.session_state.first_dealer = None
            st.rerun()
    elif mom_total > dad_total:
        st.warning(f"🏆 Νικήτρια η Μαμά: {mom_total}!")
        if st.button("Record Win & Reset"):
            st.session_state.series["Mom"] += 1
            st.session_state.scores = {"Dad": 0, "Mom": 0}
            st.session_state.history = []
            st.session_state.first_dealer = None
            st.rerun()

if st.session_state.history:
    # Showing the last 5 rounds to keep it on one screen
    st.write("**Accumulated Scores (Latest Top)**")
    st.table(st.session_state.history[::-1][:5]) 

if st.button("Reset Current Match"):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
