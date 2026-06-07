import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
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

# 3. DIRECT HARDCODED CONNECTION SETUP
# This completely bypasses Streamlit's dashboard secrets panel.

# Paste your full Google Sheet browser URL here
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_ACTUAL_SPREADSHEET_ID_HERE/edit"

# Paste your entire original service account JSON block inside the triple quotes below
SERVICE_ACCOUNT_JSON = '''
{
  "type": "service_account",
  "project_id": "mbirimba",
  "private_key_id": "4943c38d240f456c1263731fc31a9e746bf08bb4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDZ4IasoMwi7aD\n6ExtmmAVKNSKZK0Uk2ApgkJblxpOeyBSTiAosfh0AKEdDPRrbRM0YKDJ26AjL+uV\nDNb1N7Zja2V7guRSWO6h6djHp9Rrxz1pIQxOcs2ruK41Bm1xqwlv7Y+1udmfFFF6\nM+ZH+0Jnbi96pp9xOwMzwiH9vudLAwS2X0QJKsmPw774MGwY3QnNC2zE4GC06ll+\nSvCaKcnfC6340zstSRdcbnLpGd1lRKRfTOYoAMqP8gpPQ+TfHkpsLXO1iqab0JWq\nWajEJtbtNpwqXqr+1LTd+Yfw0cC0mmQDxQ/JdZ4BbFtKjkJU586TCxEY61ET2xNJ\nIel15oDNAgMBAAECggEACo6LCY+KED4GwaBJO2/9r5Ghz0rvzDlyFowCXcRkwsda\n0FeG2+v8NPgxEXVjtxy7eYxG44ues91LkvqQmnWaFaD1vfMtDAM1++q7BX5cYZOa\nuRVJ/usA5ZLNW/FZnwHTOV188sp0UWiIRlvgyGlwsE8potdhrH0NspF9w0xkXo8B\nAnYuHXMkh5XmKXKDxIWDIaPh6/YGVIoWzfEMCbtKCw5lJqOXufpZn5fUXG0ulX6T\n7yRXM/dDG1QVagJeAg2Hg8j/P0hTxkJTeAUJXNF0ao23EmyU5VpSr1X1lPUjma3M\noHF/NZ8wDtrD7yXEQkBgiXUE4WFINB5/sMxDcGfl2QKBgQDmsXnURJ5uwy3b05ML\nH25S00vR/Kh8EwSSLpLLzEoU5BHdC5Ud9EXlPYj1/SrYbVp608Uq88x2LvqenxBk\nydq/drMsYgs7BN75Iq1D1ifL9jb8198yJleqMp3WSwea5RM31SkkWunyEI72bBiK\n18VK6Y7qIjUaTP5FUpKgdCDiRwKBgQDY1wS54XmOtUXj9iXAGRreXpwcjYMpzzmm\nJXUABKGv/ZhinUUsY54MhwD3Yk1frv9pk80Rm5BRTKK5eraC/jVnGRwphGe5lgVM\nJwpWC7nVBsBDlYYHSW8DIFh+lXH+kDv0otCUx8lkpbTxn+pcJR7Xl+xj0FTUAZ40\nQAXL3+8aSwKBgD2KfNCWmZk8siAheemOsfSgb2qONzgaLq78g6agUebuzKEmNNpv\nzrGPz9ind+WSjn+TvNZvgUzJzYvBLTNl8df/x16ArTRKYV0e1g/xsl4jyZl70Qvk\n1KAPrrF7BIVatNzBHZ+YLS6pIio0vftUAkqwsbJd+8KPZYmCtKDfOeKDAoGBAMdh\nTfMso3zYqR7m4ec0LkRxcdG/PO9gn31py57so08TOt7SBRy/rD+Qkw7k0Ig+fJMz\nV8fs5lIayTUK5G6mF6xopkB2gnlevBg9fX+I4KJDxt1dyxNALlcNktEx0NNlA/v5\nCRkEauWkiC/z/qYja6yJAM72bElUA4e/ppTDnzLpAoGAPTTHz4rMeZW07OdIyktE\n9CM2sGqVjajo0VSApQgjwXnIhaSysuO5+cQLb0BUO1nl0J7ZHOhm2TB5W9iC3Amh\n07ZHSMxo4ioNLhBvhnPwU+sbpWmLQ2I6OugBbP9x+5FMyLjnMxeFbLivjCk6+Yzk\nnivRVGSLdAjtZSIZdi3h3uo=\n-----END PRIVATE KEY-----\n",
  "client_email": "mbirimba@mbirimba.iam.gserviceaccount.com",
  "client_id": "107382769538143264557",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mbirimba%40mbirimba.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'''

try:
    # Convert the text string into a native Python dictionary
    creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
    
    # Establish a manual connection explicitly feeding the credentials
    conn = st.connection(
        "gsheets",
        type=GSheetsConnection,
        spreadsheet="https://docs.google.com/spreadsheets/d/19nkWxBzNomYeP0Ls5pNMYT7ET5k05_lJagPC-fUDk1U/edit?gid=0#gid=0",
        service_account=creds_dict
    )
    
    # Read current match numbers
    df = conn.read(ttl=0) 
    series_dad = int(df.iloc[0]["Dad"])
    series_mom = int(df.iloc[0]["Mom"])
except Exception as e:
    st.error(f"Database Error: {e}")
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
            
            # Save the updated matrix using the explicit connection instance
            conn.update(data=pd.DataFrame([{"Dad": new_dad, "Mom": new_mom}]))
            
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
