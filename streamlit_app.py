import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. PAGE CONFIG & FULL-SCREEN MOBILE CSS
st.set_page_config(page_title="Biriba Tracker", layout="centered")

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
    
    /* --- THE FIX FOR "PRESS ENTER" --- */
    input {
        text-align: center;
    }
    input::placeholder {
        color: transparent !important;
    }
    input::-webkit-input-placeholder {
        color: transparent !important;
    }
    /* ---------------------------------- */
    
    </style>
    """, unsafe_allow_html=True)

# ... (Rest of the code remains the same)
