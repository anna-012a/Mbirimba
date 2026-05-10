import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. PAGE CONFIG
st.set_page_config(page_title="Biriba Tracker", layout="centered")

WINNING_SCORE = 3510

# 2. DATABASE LOAD
# We define the connection once at the top level
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Explicitly use the connection to read
    # If this fails, it falls back to defaults
    df = conn.read(worksheet="Sheet1", ttl="0") 
    series_dad = int(df.iloc[0]["Dad"])
    series_mom = int(df.iloc[0]["Mom"])
except Exception:
    series_dad, series_mom = 20, 6


# 4. HEADER
st.markdown(f"""
    <div class="scoreboard">
        <div>Dad <span style='color:#4CAF50;'>{series_dad}</span></div>
        <div>vs</div>
        <div><span style='color:#4CAF50;'>{series_mom}</span> Mom</div>
    </div>
    """, unsafe_allow_html=True)

# 5. INITIALIZE STATE
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None

# 6. WINNER LOGIC & DATABASE UPDATE
dad_total = st.session_state.scores["Dad"]
mom_total = st.session_state.scores["Mom"]

if dad_total >= WINNING_SCORE or mom_total >= WINNING_SCORE:
    winner_name = None
    if dad_total > mom_total:
        winner_name = "Dad"
        st.balloons()
        st.success(f"🏆 Νικητής ο Μπαμπάς με {dad_total}!")
    elif mom_total > dad_total:
        winner_name = "Mom"
        st.balloons()
        st.success(f"🏆 Νικήτρια η Μαμά με {mom_total}!")
    
    # Show a button to record the win in Google Sheets
    if winner_name:
        if st.button(f"Καταγραφή Νίκης για {winner_name}", use_container_width=True):
            try:
                # 1. Update the local variables
                if winner_name == "Dad":
                    new_dad = series_dad + 1
                    new_mom = series_mom
                else:
                    new_dad = series_dad
                    new_mom = series_mom + 1
                
                # 2. Create the data to upload
                # Ensure headers 'Dad' and 'Mom' match your sheet exactly
                update_df = [{"Dad": new_dad, "Mom": new_mom}]
                
                # 3. Push to Google Sheets
                conn.update(worksheet="Sheet1", data=update_df)
                
                # 4. Reset game state for next time
                st.session_state.scores = {"Dad": 0, "Mom": 0}
                st.session_state.history = []
                st.session_state.first_dealer = None
                
                st.toast("Το σκορ ενημερώθηκε στο Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating sheet: {e}")

# 7. APP CONTENT
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

# 8. TABLE & RESET
if st.session_state.history:
    st.table(st.session_state.history)

if st.button("Reset Match", use_container_width=True):
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    st.session_state.first_dealer = None
    st.rerun()
