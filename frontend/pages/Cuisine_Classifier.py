"""
Cuisine Classifier Page
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
    """Cuisine Classification Interface"""
    
    st.title("🏷️ Cuisine Classifier")
    st.markdown("Identify the **cuisine type** from a list of menu items!")
    
    st.markdown("---")
    
    # Input method
    input_method = st.radio(
        "How would you like to enter menu items?",
        ["🔤 Type manually", "☑️ Select preset menu"],
        horizontal=True
    )
    
    menu_items = ""
    
    if input_method == "🔤 Type manually":
        st.markdown("### 📝 Enter Menu Items")
        menu_items = st.text_area(
            "Enter menu items (comma or newline separated):",
            placeholder="e.g., Butter Chicken, Naan, Dal Makhani, Lassi",
            height=150,
            help="Enter the dish names you see on the restaurant menu"
        )
    
    else:
        st.markdown("### ☑️ Select a Preset Menu")
        
        preset_menus = {
            "🍛 Indian": "Butter Chicken, Naan, Dal Makhani, Biryani, Samosa, Lassi, Paneer Tikka, Gulab Jamun",
            "🍕 Italian": "Pizza, Pasta, Lasagna, Risotto, Tiramisu, Garlic Bread, Bruschetta, Cannoli",
            "🥡 Chinese": "Fried Rice, Noodles, Manchurian, Dim Sum, Spring Rolls, Wonton Soup, Chop Suey",
            "🌮 Mexican": "Tacos, Burritos, Enchiladas, Guacamole, Nachos, Quesadilla, Salsa",
            "🍔 American": "Burgers, Fries, Hot Dogs, Sandwich, Milkshake, Onion Rings, BBQ Ribs",
            "🍣 Japanese": "Sushi, Ramen, Tempura, Miso Soup, Teriyaki, Edamame, Yakitori"
        }
        
        selected_menu = st.selectbox(
            "Choose a preset menu:",
            list(preset_menus.keys())
        )
        
        menu_items = preset_menus[selected_menu]
        st.success(f"Selected: {selected_menu}")
        st.text_area("Menu items:", value=menu_items, height=150, disabled=True)
    
    st.markdown("---")
    
    # Classify button
    if st.button("🏷️ Classify Cuisine", type="primary", disabled=not menu_items):
        if not menu_items:
            st.warning("⚠️ Please enter some menu items!")
        else:
            with st.spinner("Identifying cuisine type..."):
                result = api_client.classify_cuisine(menu_items=menu_items)
            
            st.markdown("---")
            
            # Display results
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                cuisine_type = result.get('cuisine_type', 'N/A')
                confidence = result.get('confidence_score', 0)
                model_used = result.get('model_used', 'N/A')
                reasoning = result.get('reasoning', '')
                
                # Cuisine emoji mapping
                cuisine_emoji = {
                    "Indian": "🍛",
                    "Chinese": "🥡",
                    "Italian": "🍕",
                    "Mexican": "🌮",
                    "Continental": "🍽️",
                    "Italian Recipes": "🍝",
                    "North Indian Recipes": "🪔",
                    "South Indian Recipes": "🍚"
                }
                
                emoji = cuisine_emoji.get(cuisine_type, "🏷️")
                
                # Result card
                st.markdown(f"""
                <div style="
                    padding: 30px;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    margin: 10px 0;
                ">
                    <h1 style="margin: 0; font-size: 4rem;">{emoji}</h1>
                    <h2 style="margin: 10px 0 0 0;">{cuisine_type}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Details
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Confidence Score", f"{confidence:.1%}")
                
                with col2:
                    st.metric("Model Used", model_used)
                
                with col3:
                    st.metric("Items Analyzed", len(menu_items.split(',')))
                
                # Progress bar
                st.progress(confidence)
                
                # Reasoning
                if reasoning:
                    st.info(f"💡 **Why:** {reasoning}")
                
                # Show input
                st.markdown("### 📋 Menu Items Analyzed:")
                items = [item.strip() for item in menu_items.replace('\n', ',').split(',') if item.strip()]
                st.write(", ".join([f"`{item}`" for item in items]))
    
    # Tips
    st.markdown("---")
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    - Enter **5+ menu items** for more accurate classification
    - Use **authentic dish names** from the cuisine
    - The model can identify: Indian, Chinese, Italian, Mexican, Continental, and more
    """)