"""
Smart Food Ordering - Single Page Streamlit App (Clean UI)
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv

# ------------------ STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ------------------ SETUP ------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

st.set_page_config(
    page_title="Smart Food Ordering",
    page_icon="🍔",
    layout="wide"
)

# ------------------ GLOBAL STYLES ------------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem !important;
}

/* Remove default Streamlit header spacing */
header[data-testid="stHeader"] {
    height: 0px;
}

/* Extra breathing space */
section.main > div {
    padding-top: 1rem;
}

/* Fix top spacing issue */
.block-container {
    padding-top: 1.5rem;
}

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:#0E1117;
    padding:10px 20px;
    border-radius:12px;
    border:1px solid #2A2F3A;
    margin-bottom:20px;
}

/* Buttons */
div.stButton > button {
    border-radius: 8px;
    height: 40px;
    font-weight: 600;
    background-color: #1E2430;
    color: white;
    border: 1px solid #2A2F3A;
}
div.stButton > button:hover {
    border: 1px solid #FF6B35;
    color: #FF6B35;
}

/* Cards */
.card {
    background:#161A23;
    padding:25px;
    border-radius:14px;
    border:1px solid #2A2F3A;
    text-align:center;
    height:240px;
    transition: 0.3s;
}
.card:hover {
    border:1px solid #FF6B35;
    transform: translateY(-4px);
}

/* Titles */
.title {
    color:#FF6B35;
    font-size:3rem;
    text-align:center;
    margin-bottom:10px;
}
.subtitle {
    color:#CCCCCC;
    font-size:1.3rem;
    text-align:center;
}
.tagline {
    color:#AAAAAA;
    font-size:1.05rem;
    text-align:center;
}

/* Center buttons */
.center-btn {
    display:flex;
    justify-content:center;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)


# ------------------ NAVIGATION ------------------
def navigate(page):
    st.session_state.page = page
    st.rerun()


# ------------------ NAVBAR ------------------
nav1, nav2, nav3 = st.columns([1, 6, 1])

with nav1:
    if st.session_state.page != "home":
        if st.button("⬅ Back"):
            navigate("home")

with nav2:
    st.markdown(
        "<h3 style='text-align:center; color:#FF6B35; margin-top:5px;'>🍔 Smart Food Ordering</h3>",
        unsafe_allow_html=True
    )

with nav3:
    if st.session_state.page != "home":
        if st.button("🏠 Home"):
            navigate("home")

st.markdown("---")


# ------------------ FEATURE CARD ------------------
def feature_card(icon, title, desc, key, page):
    st.markdown(f"""
        <div class="card">
            <h2>{icon} {title}</h2>
            <p style="color:#BBBBBB; font-size:1.05rem;">
                {desc}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="center-btn">', unsafe_allow_html=True)
    if st.button(f"Open {title}", key=key):
        navigate(page)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ------------------ HOME ------------------
def show_home():

    # HERO
    st.markdown("""
        <div>
            <h1 class="title">🍔 Smart Food Ordering</h1>
            <p class="subtitle">
                Welcome to your <b>AI-Powered Food Ordering System</b>
            </p>
            <p class="tagline">
                Predict • Recommend • Classify • Automate — All in One Place
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ROW 1
    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "🚚", "Delivery Time",
            "Predict accurate delivery time using distance, weather, traffic, and preparation factors.",
            "delivery_btn", "delivery"
        )

    with col2:
        feature_card(
            "🍽️", "Menu Recommendation",
            "Get personalized food suggestions based on your past orders and preferences.",
            "menu_btn", "menu"
        )

    with col3:
        feature_card(
            "⭐", "Review Classification",
            "Analyze customer reviews to detect sentiment and identify genuine vs suspicious reviews.",
            "review_btn", "review"
        )

    # ROW 2 CENTERED
    col4, col5, col6 = st.columns([1,1,1])

    with col4:
        feature_card(
            "🏷️", "Cuisine Classifier",
            "Identify cuisine type automatically from menu items using AI classification.",
            "cuisine_btn", "cuisine"
        )

    with col5:
        feature_card(
            "🎫", "Support Ticketing",
            "Automatically assign customer issues to the most suitable support agent.",
            "ticket_btn", "ticket"
        )


# ------------------ ROUTER ------------------
if st.session_state.page == "home":
    show_home()

elif st.session_state.page == "delivery":
    from frontend.pages.Delivery_Time import show_page
    show_page()

elif st.session_state.page == "menu":
    from frontend.pages.Menu_Recommendation import show_page
    show_page()

elif st.session_state.page == "review":
    from frontend.pages.Review_Classification import show_page
    show_page()

elif st.session_state.page == "cuisine":
    from frontend.pages.Cuisine_Classifier import show_page
    show_page()

elif st.session_state.page == "ticket":
    from frontend.pages.Support_Ticketing import show_page
    show_page()