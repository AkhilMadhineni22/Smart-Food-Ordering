"""
Delivery Time Prediction Page
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
    """Delivery Time Prediction Interface"""
    
    st.title("🚚 Delivery Time Prediction")
    st.markdown("Predict how long it will take for your order to arrive!")
    
    st.markdown("---")
    
    # Create form for input
    with st.form("delivery_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 Delivery Details")
            distance_km = st.number_input(
                "Distance (km)",
                min_value=0.5,
                max_value=50.0,
                value=5.0,
                step=0.5,
                help="Distance from restaurant to delivery location"
            )
            
            preparation_time_min = st.number_input(
                "Preparation Time (minutes)",
                min_value=5.0,
                max_value=120.0,
                value=20.0,
                step=5.0,
                help="Time restaurant takes to prepare the order"
            )
            
            courier_experience = st.slider(
                "Courier Experience (years)",
                min_value=0.0,
                max_value=30.0,
                value=2.0,
                step=0.5
            )
        
        with col2:
            st.markdown("### 🌤️ Conditions")
            weather = st.selectbox(
                "Weather",
                ["Clear", "Rainy", "Foggy", "Windy", "Snowy"],
                help="Current weather conditions"
            )
            
            traffic_level = st.selectbox(
                "Traffic Level",
                ["Low", "Medium", "High"],
                help="Current traffic conditions"
            )
            
            time_of_day = st.selectbox(
                "Time of Day",
                ["Morning", "Afternoon", "Evening", "Night"],
                help="Time of day for delivery"
            )
            
            vehicle_type = st.selectbox(
                "Vehicle Type",
                ["Scooter", "Bike", "Car"],
                help="Delivery vehicle type"
            )
        
        st.markdown("---")
        submit_button = st.form_submit_button("🔮 Predict Delivery Time", type="primary")
    
    # Handle form submission
    if submit_button:
        with st.spinner("Predicting delivery time..."):
            result = api_client.predict_delivery_time(
                Distance_km=distance_km,
                Weather=weather,
                Traffic_Level=traffic_level,
                Time_of_Day=time_of_day,
                Vehicle_Type=vehicle_type,
                Preparation_Time_min=preparation_time_min,
                Courier_Experience_yrs=courier_experience
            )
        
        st.markdown("---")
        
        # Display results
        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            st.markdown("### 📊 Prediction Result")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Predicted Delivery Time",
                    value=f"{result.get('predicted_delivery_time_minutes', 'N/A')} min"
                )
            
            with col2:
                st.metric(
                    label="Model Used",
                    value=result.get('model_used', 'N/A')
                )
            
            with col3:
                confidence = result.get('confidence', 'N/A')
                st.metric(
                    label="Confidence",
                    value=confidence
                )
            
            # Visual indicator
            delivery_time = result.get('predicted_delivery_time_minutes', 0)
            
            if delivery_time <= 30:
                st.success("✅ Fast delivery! Your food will arrive soon.")
            elif delivery_time <= 45:
                st.info("⏱️ Moderate delivery time. Please wait.")
            else:
                st.warning("🕐 Longer delivery time. Consider ordering in advance.")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - **Clear weather** and **low traffic** result in faster deliveries
    - **Bikes/Scooters** are faster for short distances in city areas
    - **Experienced couriers** deliver more efficiently
    - **Peak hours** (lunch/dinner) may increase delivery time
    """)