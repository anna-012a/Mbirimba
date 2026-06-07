import streamlit as st
import gspread
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Biriba Tracker", layout="centered")

# 2. UI STYLING (CSS)
st.markdown("""
    <style>
    .block-container { padding-top: 0rem !important; max-width: 100% !important; text-align: center; }
    header, footer {visibility: hidden;}
    .scoreboard {
        text-align: center; font-size: 24px; font-weight: bold; background-color: #1E1E1E;
        padding: 15px 5px; border-radius: 0px 0px 15px 15px; border: 2px solid #4CAF50;
        margin-bottom: 15px; display: flex; justify-content: space-around; align-items: center; color: white;
    }
    th, td { text-align: center !important; }
    input { text-align: center; }
    input::placeholder { color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SECURE DATABASE CONNECTION
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/19nkWxBzNomYeP0Ls5pNMYT7ET5k05_lJagPC-fUDk1U/edit?gid=0"

try:
    # Safely load the credentials string directly from Streamlit's secure vault
    raw_creds = st.secrets["my_creds"]
    creds_dict = json.loads(raw_creds)
    
    # Force fix any line break anomalies safely inside memory
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    # Authenticate via gspread using the fresh credentials dict
    gc = gspread.service_account_from_dict(creds_dict)
    sh = gc.open_by_url(SPREADSHEET_URL)
    worksheet = sh.get_worksheet(0) 
    
    # Read series statistics
    records = worksheet.get_all_records()
    series_dad = int(records[0]["Dad"])
    series_mom = int(records[0]["Mom"])
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    series_dad, series_mom = 20, 6

# 4. HEADER
st.markdown(f"""
    <div class="scoreboard">
        <div>Dad <span style='color:#4CAF50;'>{series_dad}</span></div>
        <div>vs</div>
        <div><span style='color:#4CAF50;'>{series_mom}</span> Mom</div>
    </div>
    """, unsafe_allow_html=True)

# 5. INITIALIZE MATCH STATE
if 'scores' not in st.session_state:
    st.session_state.scores, st.session_state.history, st.session_state.first_dealer = {"Dad": 0, "Mom": 0}, [], None

WINNING_SCORE = 3510
dad_total, mom_total = st.session_state.scores["Dad"], st.session_state.scores["Mom"]

# 6. WINNER LOGIC
if dad_total >= WINNING_SCORE or mom_total >= WINNING_SCORE:
    winner = "Dad" if dad_total > mom_total else "Mom"
    st.balloons()
    st.success(f"🏆 Νικητής: {winner} ({max(dad_total, mom_total)})")
    
    if st.button(f"Save Win for {winner} to Excel", use_container_width=True):
        try:
            new_dad = series_dad + 1 if winner == "Dad" else series_dad
            new_mom = series_mom + 1 if winner == "Mom" else series_mom
            
            # Commit directly to spreadsheet structure coordinates
            worksheet.update_acell('A2', new_dad)
            worksheet.update_acell('B2', new_mom)
            
            st.session_state.scores, st.session_state.history, st.session_state.first_dealer = {"Dad": 0, "Mom": 0}, [], None
            st.rerun()
        except Exception as e:
            st.error(f"Save Failed: {e}")

# 7. GAMEPLAY UI
round_num = len(st.session_state.history) + 1
if st.session_state.first_dealer is None:
    st.subheader("Ποιος μοιράζει πρώτος;")
    c1, c2 = st.columns(2)
    if c1.button("Μπαμπάς", use_container_width=True): st.session_state.first_dealer = "Dad"; st.rerun()
    if c2.button("Μαμά", use_container_width=True): st.session_state.first_dealer = "Mom"; st.rerun()
else:
    players = ["Dad", "Mom"] if st.session_state.first_dealer == "Dad" else ["Mom", "Dad"]
    dealer = players[0] if round_num % 2 != 0 else players[1]
    st.markdown(f"### Γύρος {round_num} | 🃏 {dealer} μοιράζει")
    with st.form("score_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([3, 3, 2])
        d_pts = f1.number_input("Dad", step=5, value=0)
        m_pts = f2.number_input("Mom", step=5, value=0)
        if f3.form_submit_button("OK", use_container_width=True):
            st.session_state.scores["Dad"] += d_pts
            st.session_state.scores["Mom"] += m_pts
            st.session_state.history.append({"Rd": round_num, "Dad Total": st.session_state.scores["Dad"], "Mom Total": st.session_state.scores["Mom"]})
            st.rerun()

# 8. HISTORY & RESET
if st.session_state.history:
    st.table(st.session_state.history)
if st.button("Reset Match (No Save)", use_container_width=True):
    st.session_state.scores, st.session_state.history, st.session_state.first_dealer = {"Dad": 0, "Mom": 0}, [], None
    st.rerun()
