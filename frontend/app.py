import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
from io import BytesIO
import time
# Page configuration
st.set_page_config(
    page_title="🛰️ AeroPrice - Satellite Property Valuation",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🛰️"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #00d4ff;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
    }
    
    .metric-card {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #2E8B57;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .chart-container {
        background: rgba(26, 26, 46, 0.6);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(26, 26, 46, 0.8);
        border: 1px solid #00d4ff;
        border-radius: 5px;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #2E8B57 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        font-size: 18px;
        color: #00d4ff;
    }
    
    .error-message {
        background: rgba(220, 20, 60, 0.2);
        border: 1px solid #DC143C;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        color: #ff6b6b;
    }
    
    .success-message {
        background: rgba(46, 139, 87, 0.2);
        border: 1px solid #2E8B57;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        color: #90EE90;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'properties' not in st.session_state:
    st.session_state.properties = []
if 'selected_property' not in st.session_state:
    st.session_state.selected_property = None
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = None
if 'explanation_results' not in st.session_state:
    st.session_state.explanation_results = None

# API configuration
API_BASE_URL = "http://localhost:5000"

def load_properties():
    """Load properties from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/properties", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to load properties: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return []

def predict_property(property_index):
    """Predict property price using the API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"property_index": property_index},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Prediction failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

def explain_property(property_index):
    """Get property explanation using the API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/explain_prediction",
            json={"property_index": property_index},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Explanation failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None

def create_contribution_chart(contributions):
    """Create interactive contribution chart."""
    if not contributions:
        return None
    
    features = list(contributions.keys())
    values = list(contributions.values())
    
    # Format feature names
    formatted_features = [f.replace('_', ' ').title() for f in features]
    
    # Create colors based on positive/negative values
    colors = ['#2E8B57' if x >= 0 else '#DC143C' for x in values]
    
    fig = go.Figure(data=[
        go.Bar(
            y=formatted_features,
            x=values,
            orientation='h',
            marker_color=colors,
            text=[f'${v:,.0f}' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Price Impact: $%{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Feature Contributions to Property Value",
        xaxis_title="Price Impact ($)",
        yaxis_title="Features",
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        height=400
    )
    
    # Add zero line
    fig.add_vline(x=0, line_dash="dash", line_color="white", opacity=0.5)
    
    return fig

def create_scores_radar_chart(scores):
    """Create radar chart for scores."""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Property Scores',
        line_color='#00d4ff',
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickcolor='white',
                gridcolor='rgba(255, 255, 255, 0.3)'
            ),
            angularaxis=dict(
                tickcolor='white',
                gridcolor='rgba(255, 255, 255, 0.3)'
            )
        ),
        showlegend=True,
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig

# Main app layout
st.title("🛰️ AeroPrice - Satellite Property Valuation")
st.markdown("**AI-Powered Property Analysis using Satellite Imagery**")

# Sidebar for property selection
with st.sidebar:
    st.header("🏠 Property Selection")
    
    # Load properties button
    if st.button("🔄 Load Properties", type="primary"):
        with st.spinner("Loading properties..."):
            st.session_state.properties = load_properties()
            if st.session_state.properties:
                st.success(f"Loaded {len(st.session_state.properties)} properties!")
    
    # Property selector
    if st.session_state.properties:
        property_options = {
            f"{prop['streetAddress']}, {prop['zipcode']} (ID: {prop['id']})": prop['id'] 
            for prop in st.session_state.properties[:100]  # Limit for performance
        }
        
        selected_address = st.selectbox(
            "Select a property:",
            options=list(property_options.keys()),
            index=0
        )
        
        if selected_address:
            st.session_state.selected_property = property_options[selected_address]
            st.info(f"Selected Property ID: {st.session_state.selected_property}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Analysis")
    
    if st.session_state.selected_property is not None:
        if st.button("🔍 Analyze Property", type="primary", use_container_width=True):
            with st.spinner("Analyzing satellite imagery..."):
                # Get prediction
                prediction_results = predict_property(st.session_state.selected_property)
                if prediction_results:
                    st.session_state.prediction_results = prediction_results
                    st.success("✅ Analysis complete!")
                else:
                    st.error("❌ Analysis failed!")
        
        # Display prediction results
        if st.session_state.prediction_results:
            results = st.session_state.prediction_results
            
            # Main prediction card
            st.markdown(f"""
            <div class='prediction-card'>
                <h2>💰 Predicted Price: ${results.get('predicted_price', 0):,.0f}</h2>
                <p><strong>Actual Price:</strong> ${results.get('actual_price', 'N/A'):,.0f if results.get('actual_price') else 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Scores in columns
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>🏘️ Neighborhood</h4>
                    <h3>{results.get('neighborhood_score', 0):.1f}/10</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>🚗 Accessibility</h4>
                    <h3>{results.get('accessibility_score', 0):.1f}/10</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col_c:
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>🌳 Green Space</h4>
                    <h3>{results.get('green_space_score', 0):.1f}/10</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Radar chart for scores
            scores = {
                'Neighborhood': results.get('neighborhood_score', 0),
                'Accessibility': results.get('accessibility_score', 0),
                'Green Space': results.get('green_space_score', 0)
            }
            
            radar_chart = create_scores_radar_chart(scores)
            if radar_chart:
                st.plotly_chart(radar_chart, use_container_width=True)

with col2:
    st.header("🛰️ Satellite Image")
    
    if st.session_state.prediction_results and st.session_state.prediction_results.get('satellite_image'):
        # Display satellite image
        image_data = st.session_state.prediction_results['satellite_image']
        if image_data.startswith('data:image'):
            st.image(image_data, caption="Analyzed Satellite View", use_column_width=True)
        
        # Display image metadata
        metadata = st.session_state.prediction_results.get('image_metadata', {})
        if metadata:
            st.markdown("**📍 Image Details:**")
            st.write(f"**Location:** {metadata.get('location', 'Unknown')}")
            st.write(f"**Resolution:** {metadata.get('resolution', 'Unknown')}")
            st.write(f"**Capture Date:** {metadata.get('capture_date', 'Unknown')}")
    else:
        st.info("👆 Select and analyze a property to view satellite imagery")

# Explanation section
if st.session_state.selected_property is not None:
    st.header("📝 Detailed Explanation")
    
    if st.button("🧠 Get Detailed Explanation", type="primary", use_container_width=True):
        with st.spinner("Generating detailed explanation..."):
            explanation_results = explain_property(st.session_state.selected_property)
            if explanation_results:
                st.session_state.explanation_results = explanation_results
                st.success("✅ Explanation generated!")
            else:
                st.error("❌ Explanation generation failed!")
    
    # Display explanation results
    if st.session_state.explanation_results:
        results = st.session_state.explanation_results
        
        # Summary text
        if results.get('summary_text'):
            st.markdown(f"""
            <div class='prediction-card'>
                <h3>📋 Analysis Summary</h3>
                <p style='white-space: pre-line;'>{results['summary_text']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Contributions chart
        if results.get('contributions'):
            st.markdown("### 📊 Feature Contributions")
            contrib_chart = create_contribution_chart(results['contributions'])
            if contrib_chart:
                st.plotly_chart(contrib_chart, use_container_width=True)
        
        # Inferred amenities
        if results.get('inferred_amenities'):
            st.markdown("### 🏫 Inferred Amenities")
            amenities = results['inferred_amenities']
            
            for amenity, details in amenities.items():
                confidence_color = {
                    'high': '#2E8B57',
                    'moderate': '#FFD93D', 
                    'low': '#DC143C'
                }.get(details.get('confidence', 'low'), '#DC143C')
                
                st.markdown(f"""
                <div style='background: rgba(26, 26, 46, 0.6); border-left: 4px solid {confidence_color}; padding: 10px; margin: 5px 0; border-radius: 5px;'>
                    <strong>{amenity.replace('_', ' ').title()}:</strong> {details.get('proximity', 'Unknown')}
                    <br><small style='color: #888;'>{details.get('reasoning', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts section
        if results.get('charts'):
            st.markdown("### 📈 Detailed Charts")
            
            charts = results['charts']
            for i, chart in enumerate(charts):
                with st.expander(f"📊 {chart.get('title', 'Chart')}"):
                    st.write(chart.get('description', ''))
                    
                    # Try to load chart image
                    chart_url = chart.get('url', '')
                    if chart_url and not chart_url.endswith('placeholder.png'):
                        try:
                            # For local development, construct full URL
                            full_url = f"{API_BASE_URL}{chart_url}"
                            response = requests.get(full_url, timeout=10)
                            if response.status_code == 200:
                                st.image(response.content, use_column_width=True)
                            else:
                                st.info("Chart image not available yet.")
                        except:
                            st.info("Chart image not available yet.")
                    else:
                        st.info("Chart generation in progress...")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>🛰️ <strong>AeroPrice</strong> - AI-Powered Property Valuation using Satellite Imagery</p>
    <p>Built with TensorFlow, Flask, and Streamlit</p>
</div>
""", unsafe_allow_html=True)
