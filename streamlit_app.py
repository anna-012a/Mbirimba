import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Biriba", layout="centered")

# CSS for the custom header and to save space
st.markdown("""
    <style>
    .block-container {padding-top: 1rem;}
    .scoreboard {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. DATABASE CONNECTION
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Adjust 'Sheet1' to the name of your worksheet
    df = conn.read(worksheet="Sheet1", ttl="0") 
    series_dad = int(df.iloc[0]["Dad"])
    series_mom = int(df.iloc[0]["Mom"])
except:
    # Fallback if Google Sheets isn't ready yet
    series_dad, series_mom = 20, 6

# 2. THE HEADER (Your Drawing)
st.markdown(f"""
    <div class="scoreboard">
        Dad <span style='color:#4CAF50;'>{series_dad}</span> &nbsp;&nbsp; vs &nbsp;&nbsp; <span style='color:#4CAF50;'>{series_mom}</span> Mom
    </div>
    """, unsafe_allow_html=True)

# 3. GAME STATE
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None

# 4. DEALER SELECTION
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
    # Role Logic
    players = ["Dad", "Mom"] if st.session_state.first_dealer == "Dad" else ["Mom", "Dad"]
    current_dealer = players[0] if round_num % 2 != 0 else players[1]
    
    st.write(f"🎮 **Γύρος {round_num}** | 🃏 **{current_dealer}** μοιράζει")

    # Score Input
    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        d_pts = f1.number_input("Dad", step=5, value=0)
        m_pts = f2.number_input("Mom", step=5, value=0)
        if f3.form_submit_button("OK"):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({
                "Dad Total": st.session_state.scores["Dad"], 
                "Mom Total": st.session_state.scores["Mom"]
            })
            st.rerun()

# 5. TABLE & RESET
if st.session_state.history:
    st.table(st.session_state.history[::-1][:5])

if st.button("Reset Current Match"):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
