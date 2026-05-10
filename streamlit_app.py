import streamlit as st

# Force the app to be wide and remove top padding
st.set_page_config(page_title="Biriba", layout="centered")

st.markdown("""
    <style>
    /* This removes the massive gap at the top of Streamlit apps */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;} /* Hides the 'Made with Streamlit' top bar */
    
    .scoreboard {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background-color: #1E1E1E;
        padding: 15px 5px;
        border-radius: 0px 0px 15px 15px; /* Rounded bottom corners */
        border: 2px solid #4CAF50;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Update your header HTML to use the 'flex' layout for better spacing
st.markdown(f"""
    <div class="scoreboard">
        <div>Dad <span style='color:#4CAF50;'>{series_dad}</span></div>
        <div>vs</div>
        <div><span style='color:#4CAF50;'>{series_mom}</span> Mom</div>
    </div>
    """, unsafe_allow_html=True)
