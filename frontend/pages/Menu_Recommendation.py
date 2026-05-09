"""
Menu Recommendation Page
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
    """Menu Recommendation Interface"""
    
    st.title("🍽️ Menu Recommendation")
    st.markdown("Get personalized dish recommendations based on your order history!")
    
    st.markdown("---")
    
    # Sample menu items for reference
    sample_items = [
        "Butter Chicken", "Pizza", "Biryani", "Pasta", "Noodles",
        "Dal Makhani", "Dosa", "Idli", "Samosa", "Burgers",
        "Salad", "Fried Rice", "Manchurian", "Paneer Tikka",
        "Tandoori Chicken", "Momos", "Lasagna", "Tacos", "Shawarma"
    ]
    
    # Input method selection
    input_method = st.radio(
        "How would you like to enter your past orders?",
        ["🔤 Type manually", "☑️ Select from list"],
        horizontal=True
    )
    
    past_orders = []
    
    if input_method == "🔤 Type manually":
        st.markdown("### 📝 Enter Your Past Orders")
        order_input = st.text_area(
            "Enter your past order items (comma-separated)",
            placeholder="e.g., Butter Chicken, Pizza, Biryani",
            height=100
        )
        
        if order_input:
            past_orders = [item.strip() for item in order_input.split(",") if item.strip()]
    
    else:
        st.markdown("### ☑️ Select Your Past Orders")
        selected = st.multiselect(
            "Choose items you've ordered before:",
            sample_items,
            default=[]
        )
        past_orders = selected
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Get Recommendation", type="primary", disabled=len(past_orders) == 0):
        if len(past_orders) == 0:
            st.warning("⚠️ Please enter at least one past order!")
        else:
            with st.spinner("Analyzing your preferences..."):
                result = api_client.recommend_menu(past_orders)
            
            st.markdown("---")
            
            # Display results
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                st.markdown("### 🎯 Recommended For You")
                
                # Display recommended item prominently
                recommended = result.get('recommended_item', 'N/A')
                confidence = result.get('confidence_score', 0)
                model_used = result.get('model_used', 'N/A')
                reasoning = result.get('reasoning', '')
                
                # Create a nice card for the recommendation
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        color: white;
                        text-align: center;
                        margin: 10px 0;
                    ">
                        <h2 style="margin: 0; font-size: 2.5rem;">{recommended}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Confidence Score", f"{confidence:.1%}")
                    st.metric("Model", model_used)
                
                # Reasoning
                if reasoning:
                    st.info(f"💡 **Why this recommendation:** {reasoning}")
                
                # Confidence visualization
                st.progress(confidence)
                st.caption(f"Confidence: {confidence:.1%}")
                
                # Your input summary
                st.markdown("### 📋 Based on your orders:")
                st.write(", ".join([f"`{item}`" for item in past_orders]))
    
    # Show sample suggestions when no input
    if len(past_orders) == 0:
        st.markdown("---")
        st.markdown("### 💡 Try these examples:")
        st.markdown("""
        - **Indian food lover:** Butter Chicken, Biryani, Dal Makhani, Dosa
        - **Pizza & Pasta fan:** Pizza, Pasta, Lasagna, Garlic Bread
        - **Asian cuisine:** Noodles, Fried Rice, Momos, Manchurian
        - **Fast food:** Burgers, Pizza, Fries, Momos
        """)