import streamlit as st

st.set_page_config(page_title="Μπιρίμπα Score", page_icon="🃏")

WINNING_SCORE = 3510

# Initialize State
if 'scores' not in st.session_state:
    st.session_state.scores = {"Dad": 0, "Mom": 0}
    st.session_state.history = []
    # Initialize series wins (Update these numbers to their current record)
    if 'series' not in st.session_state:
        st.session_state.series = {"Dad": 20, "Mom": 6}

st.title("🃏 Μπιρίμπα Tracker")

# --- SIDEBAR: LIFE-TIME WINS ---
st.sidebar.header("🏆 Συνολικό Σκορ (Wins)")
st.sidebar.metric("Dad", st.session_state.series["Dad"])
st.sidebar.metric("Mom", st.session_state.series["Mom"])

if st.sidebar.button("Edit Series Score"):
    # Optional: logic to manually adjust the 20 vs 6
    pass

# --- ROLES LOGIC ---
round_num = len(st.session_state.history) + 1
# Alternating roles based on round count
if round_num % 2 != 0:
    dealer, mbiribakia = "Dad", "Mom"
else:
    dealer, mbiribakia = "Mom", "Dad"

st.subheader(f"Γύρος {round_num}")
c1, c2 = st.columns(2)
c1.info(f"**Μοιράζει:**\n\n{dealer}")
c2.success(f"**Μπιριμπάκια:**\n\n{mbiribakia}")

# --- SCORE INPUT ---
with st.form("score_entry", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    val_dad = col_a.number_input("Πόντοι Μπαμπά", step=5, value=0)
    val_mom = col_b.number_input("Πόντοι Μαμάς", step=5, value=0)
    
    if st.form_submit_button("Προσθήκη Πόντων"):
        st.session_state.scores["Dad"] += val_dad
        st.session_state.scores["Mom"] += val_mom
        st.session_state.history.append({"Γύρος": round_num, "Dad": val_dad, "Mom": val_mom})
        st.rerun()

# --- WINNER LOGIC ---
dad_total = st.session_state.scores["Dad"]
mom_total = st.session_state.scores["Mom"]

st.divider()
st.header(f"Σύνολο: {dad_total} — {mom_total}")

if dad_total >= WINNING_SCORE or mom_total >= WINNING_SCORE:
    if dad_total > mom_total:
        winner = "Dad"
        st.balloons()
        st.warning(f"🏆 Νικητής ο Μπαμπάς με {dad_total}!")
    elif mom_total > dad_total:
        winner = "Mom"
        st.balloons()
        st.warning(f"🏆 Νικήτρια η Μαμά με {mom_total}!")
    else:
        st.info("Ισοπαλία πάνω από το όριο! Συνεχίστε άλλον έναν γύρο.")
    
    if st.button("Καταγραφή Νίκης & Νέο Παιχνίδι"):
        st.session_state.series[winner] += 1
        st.session_state.scores = {"Dad": 0, "Mom": 0}
        st.session_state.history = []
        st.rerun()

# --- HISTORY ---
if st.session_state.history:
    with st.expander("Δείτε το ιστορικό των γύρων"):
        st.table(st.session_state.history)
