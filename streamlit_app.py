import streamlit as st

# Force a clean mobile layout
st.set_page_config(page_title="Biriba", layout="centered")

# Custom CSS to reduce padding and keep it on one screen
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    div[data-testid="stMetricValue"] {font-size: 24px;}
    </style>
    """, unsafe_all_tags=True)

if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.series = {"Dad": 20, "Mom": 6}
    st.session_state.first_dealer = None

# 1. TOP HEADER: Overall Series Score (Dad 20 vs 6 Mom)
c1, c2 = st.columns(2)
c1.metric("Dad Series", st.session_state.series["Dad"])
c2.metric("Mom Series", st.session_state.series["Mom"])

st.divider()

# 2. DEALER SELECTION / ROLE DISPLAY
round_num = len(st.session_state.history) + 1

if st.session_state.first_dealer is None:
    st.subheader("Ποιος μοιράζει πρώτος;")
    col_a, col_b = st.columns(2)
    if col_a.button("Μπαμπάς"):
        st.session_state.first_dealer = "Dad"
        st.rerun()
    if col_b.button("Μαμά"):
        st.session_state.first_dealer = "Mom"
        st.rerun()
else:
    # Logic to alternate roles based on the first dealer chosen
    players = ["Dad", "Mom"] if st.session_state.first_dealer == "Dad" else ["Mom", "Dad"]
    # Even rounds swap roles
    current_dealer = players[0] if round_num % 2 != 0 else players[1]
    current_mbiribakia = players[1] if round_num % 2 != 0 else players[0]
    
    st.write(f"**Γύρος {round_num}** | 🃏 **{current_dealer}** μοιράζει")

    # 3. SCORE INPUT (Compact)
    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        d_pts = f1.number_input("Dad", step=5, format="%d")
        m_pts = f2.number_input("Mom", step=5, format="%d")
        if f3.form_submit_button("OK"):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({
                "Dad": st.session_state.scores["Dad"], 
                "Mom": st.session_state.scores["Mom"]
            })
            st.rerun()

# 4. ACCUMULATED TABLE (Fixed height to prevent scrolling)
if st.session_state.history:
    st.write("**Accumulated Scores**")
    # Reverse history to show latest rounds at the top
    st.dataframe(st.session_state.history[::-1], use_container_width=True, height=200)

# Reset Match
if st.button("New Match", use_container_width=True):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
