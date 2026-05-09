"""
Review Classification Page
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
    """Review Classification Interface"""
    
    st.title("⭐ Review Classification")
    st.markdown("Detect whether a restaurant review is **genuine** or **fake**!")
    
    st.markdown("---")
    
    # Create two columns for input
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 Enter Review Details")
        
        rating = st.slider(
            "Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.0,
            step=0.5,
            help="Restaurant rating (1-5 stars)"
        )
        
        # Show stars visualization
        stars = "⭐" * int(rating)
        if rating % 1 != 0:
            stars += "½"
        st.markdown(f"**Selected Rating:** {stars} ({rating}/5)")
    
    with col2:
        st.markdown("### 📄 Review Text")
        
        review_text = st.text_area(
            "Enter the restaurant review:",
            placeholder="e.g., Amazing food! Best butter chicken I've ever had...",
            height=150
        )
    
    st.markdown("---")
    
    # Sample reviews for quick testing
    with st.expander("📚 Try sample reviews"):
        st.markdown("### Genuine Reviews:")
        genuine_samples = [
            "The food was decent but the service was slow. Would not recommend for lunch breaks.",
            "Good quality ingredients, portions were a bit smaller than expected. Overall okay experience.",
            "Nice ambiance and friendly staff. The biryani was flavorful but a bit too spicy for my taste."
        ]
        
        st.markdown("### Fake/Suspicious Reviews:")
        fake_samples = [
            "BEST RESTAURANT EVER!!! Everything was perfect!!! 5 stars!!!",
            "Amazing food! Best service! Highly recommend! Must try!",
            "Perfect in every way! Never disappoints! Everyone should visit!"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Genuine samples:**")
            for i, sample in enumerate(genuine_samples, 1):
                if st.button(f"Use Genuine #{i}", key=f"genuine_{i}"):
                    st.session_state.sample_review = sample
                    st.session_state.sample_rating = 3.5
        
        with col2:
            st.markdown("**Fake samples:**")
            for i, sample in enumerate(fake_samples, 1):
                if st.button(f"Use Fake #{i}", key=f"fake_{i}"):
                    st.session_state.sample_review = sample
                    st.session_state.sample_rating = 5.0
    
    # Check for session state sample
    if "sample_review" in st.session_state:
        review_text = st.session_state.sample_review
        rating = st.session_state.sample_rating
        st.success(f"📋 Loaded sample review (Rating: {rating})")
    
    # Classify button
    if st.button("🔍 Classify Review", type="primary", disabled=not review_text):
        if not review_text:
            st.warning("⚠️ Please enter a review text!")
        else:
            with st.spinner("Analyzing review..."):
                result = api_client.classify_review(
                    rating=rating,
                    review_text=review_text
                )
            
            st.markdown("---")
            
            # Display results
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                sentiment = result.get('sentiment', None)
                confidence = result.get('confidence', 0)
                model_used = result.get('model', 'N/A')
                reason = result.get('reason', '')
                
                # Result card
                if sentiment is not None:
                    if sentiment == "Positive":
                        st.markdown(f"""
                        <div style="
                            padding: 30px;
                            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                            border-radius: 15px;
                            color: white;
                            text-align: center;
                            margin: 10px 0;
                        ">
                            <h2 style="margin: 0;">✅ {sentiment}</h2>
                            <p style="margin: 10px 0 0 0;">This appears to be an authentic customer review</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            padding: 30px;
                            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                            border-radius: 15px;
                            color: white;
                            text-align: center;
                            margin: 10px 0;
                        ">
                            <h2 style="margin: 0;">⚠️ {sentiment}</h2>
                            <p style="margin: 10px 0 0 0;">This review appears to be negative and suspicious/fake</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Details
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Confidence Score", f"{confidence:.1%}")
                    
                    with col2:
                        st.metric("Model Used", model_used)
                    
                    with col3:
                        st.metric("Rating Given", f"{rating}/5")
                    
                    # Progress bar
                    st.progress(confidence)
                    
                    # Reason
                    if reason:
                        st.info(f"💡 **Analysis:** {reason}")
                    
                    # Show the reviewed text
                    st.markdown("### 📄 Reviewed Text:")
                    st.text(review_text)
    
    st.markdown("---")
    st.markdown("### 💡 How it works")
    st.markdown("""
    The AI model analyzes:
    - **Text patterns** - Excessive punctuation, repetitive words, generic language
    - **Rating consistency** - Whether the text matches the given rating
    - **Sentiment analysis** - Genuine reviews usually have balanced opinions
    """)