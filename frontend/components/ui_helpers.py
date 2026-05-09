"""
UI Helper functions for Streamlit frontend
"""
import streamlit as st


def show_success(message: str):
    """Display success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Display error message"""
    st.error(f"❌ {message}")


def show_warning(message: str):
    """Display warning message"""
    st.warning(f"⚠️ {message}")


def show_info(message: str):
    """Display info message"""
    st.info(f"ℹ️ {message}")


def loading_spinner(message: str = "Loading..."):
    """Create a loading spinner"""
    return st.spinner(message)


def create_metric_card(label: str, value: str, delta: str = None):
    """Create a metric card"""
    st.metric(label=label, value=value, delta=delta)


def create_result_card(title: str, value: str, emoji: str = "✅", style: str = "success"):
    """Create a styled result card"""
    colors = {
        "success": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
        "error": "linear-gradient(135deg, #eb3349 0%, #f45c43 100%)",
        "info": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "warning": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    }
    
    bg_color = colors.get(style, colors["success"])
    
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: {bg_color};
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    ">
        <h2 style="margin: 0;">{emoji} {title}</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.5rem;">{value}</p>
    </div>
    """, unsafe_allow_html=True)


def show_api_status(base_url: str):
    """Show API connection status in sidebar"""
    import requests
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=3)
        if response.status_code == 200:
            st.sidebar.success("🟢 Backend Connected")
            return True
    except:
        pass
    
    st.sidebar.error("🔴 Backend Disconnected")
    st.sidebar.info("Start FastAPI: `uvicorn app.main:app`")
    return False