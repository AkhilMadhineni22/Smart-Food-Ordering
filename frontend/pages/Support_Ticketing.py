"""
Support Ticketing Page
"""
import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from frontend.components.api_clients import api_client


def show_page():
    """Smart Ticketing Interface"""
    
    st.title("🎫 Support Ticketing")
    st.markdown("Automatically **route customer issues** to the right support team!")
    
    st.markdown("---")
    
    # Input
    st.markdown("### 📝 Describe the Issue")
    
    issue_text = st.text_area(
        "Enter the customer issue or complaint:",
        placeholder="e.g., My order arrived cold and late. The burger was missing from my order...",
        height=150,
        help="Describe the customer's problem in detail"
    )
    
    # Sample issues for quick testing
    with st.expander("📚 Try sample issues"):
        sample_issues = [
            ("Order Problem", "My order arrived missing items. The fries were not included."),
            ("Delivery Problem", "The delivery person was rude and delivered the food very late."),
            ("Payment Issue", "I was charged twice for my order. Please refund the extra amount."),
            ("Food Quality", "The pizza was cold and the toppings were stale. Very disappointed."),
            ("Account Issue", "I cannot login to my account. It shows invalid credentials error."),
            ("Delivery Address", "The driver delivered to the wrong address. My food is gone.")
        ]
        
        for i, (category, issue) in enumerate(sample_issues, 1):
            if st.button(f"Use: {category}", key=f"issue_{i}"):
                st.session_state.sample_issue = issue
    
    # Check for session state sample
    if "sample_issue" in st.session_state:
        issue_text = st.session_state.sample_issue
        st.success("📋 Loaded sample issue")
    
    st.markdown("---")
    
    # Assign button
    if st.button("🎫 Assign to Team", type="primary", disabled=not issue_text):
        if not issue_text:
            st.warning("⚠️ Please describe the issue!")
        else:
            with st.spinner("Analyzing and routing the ticket..."):
                result = api_client.assign_ticket(issue_text=issue_text)
            
            st.markdown("---")
            
            # Display results
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                agent = result.get('assigned_agent', 'N/A')
                confidence = result.get('confidence_score', 0)
                model_used = result.get('model_used', 'N/A')
                reasoning = result.get('reason', '')
                
                # Team emoji mapping
                team_emoji = {
                    "Delivery Team": "🚚",
                    "Kitchen Team": "👨‍🍳",
                    "Customer Support": "📞",
                    "Technical Team": "💻",
                    "Management": "👔",
                    "Refund Team": "💰"
                }
                
                emoji = team_emoji.get(agent, "🎫")
                
                # Result card
                st.markdown(f"""
                        <div style="
                            padding: 30px;
                            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            border-radius: 15px;
                            color: white;
                            text-align: center;
                            margin: 10px 0;
                        ">
                            <h1 style="margin: 0; font-size: 4rem;">{emoji}</h1>
                            <h2 style="margin: 10px 0 0 0;">👤 {agent}</h2>
                            <p style="margin: 10px 0 0 0;">Ticket Assigned</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Details
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Confidence Score", f"{confidence:.1%}")
                
                with col2:
                    st.metric("Model Used", model_used)
                
                with col3:
                    st.metric("Status", "Assigned")
                
                # Progress bar
                st.progress(confidence)
                
                # Reasoning
                if reasoning:
                    st.info(f"💡 **Why this team:** {reasoning}")
                
                # Show input
                st.markdown("### 📋 Issue Description:")
                st.text(issue_text)
    
    # Team info
    st.markdown("---")
    st.markdown("### 📋 Support Teams")
    
    teams = {
        "🚚 Delivery Team": "Delivery issues, late orders, wrong address",
        "👨‍🍳 Kitchen Team": "Food quality, missing items, wrong order",
        "📞 Customer Support": "General inquiries, account issues",
        "💻 Technical Team": "App bugs, login issues, payment errors",
        "💰 Refund Team": "Refunds, billing disputes, charges"
    }
    
    for team, desc in teams.items():
        st.markdown(f"**{team}** - {desc}")
    
    st.markdown("---")
    st.markdown("### 💡 How it works")
    st.markdown("""
    The AI analyzes the issue description and automatically:
    1. **Identifies the problem type** - delivery, food quality, payment, etc.
    2. **Routes to the right team** - ensures faster resolution
    3. **Provides reasoning** - explains why that team was selected
    """)