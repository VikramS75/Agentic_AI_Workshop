# location_enhanced_app.py - With Google Places API integration
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import requests
import json
from typing import List, Dict
import time
from fpdf import FPDF
import re

# === HARDCODED API KEYS ===
GEMINI_API_KEY = "AIzaSyC7K1mPTvB9WDVC06u31HlkvBzH0hMOdbA"
GOOGLE_PLACES_API_KEY = "AIzaSyCSJ_jYL8MJ1E0ibQsdLToLl4IyzaAYoec"

# Configure Streamlit
st.set_page_config(
    page_title="Clothing Store Competitor Intelligence",
    page_icon="👗",
    layout="wide"
)

def get_nearby_clothing_stores(api_key: str, location: str, radius: int = 5000) -> List[Dict]:
    """Get nearby clothing stores using Google Places API"""
    try:
        # First, get coordinates for the location
        geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocoding_params = {
            'address': location,
            'key': api_key
        }
        
        geo_response = requests.get(geocoding_url, params=geocoding_params)
        geo_data = geo_response.json()
        
        if geo_data['status'] != 'OK' or not geo_data['results']:
            return []
        
        # Get coordinates
        lat = geo_data['results'][0]['geometry']['location']['lat']
        lng = geo_data['results'][0]['geometry']['location']['lng']
        
        # Search for nearby clothing stores
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places_params = {
            'location': f"{lat},{lng}",
            'radius': radius,
            'type': 'clothing_store',
            'key': api_key
        }
        
        places_response = requests.get(places_url, params=places_params)
        places_data = places_response.json()
        
        stores = []
        if places_data['status'] == 'OK':
            for place in places_data['results'][:15]:  # Limit to 15 stores
                # Get detailed information
                details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                details_params = {
                    'place_id': place['place_id'],
                    'fields': 'name,formatted_address,rating,price_level,opening_hours,website,formatted_phone_number,photos',
                    'key': api_key
                }
                
                details_response = requests.get(details_url, params=details_params)
                details_data = details_response.json()
                
                if details_data['status'] == 'OK':
                    store_info = details_data['result']
                    stores.append({
                        'name': store_info.get('name', 'Unknown'),
                        'address': store_info.get('formatted_address', 'Address not available'),
                        'rating': store_info.get('rating', 'No rating'),
                        'price_level': store_info.get('price_level', 'Unknown'),
                        'phone': store_info.get('formatted_phone_number', 'Not available'),
                        'website': store_info.get('website', 'Not available'),
                        'opening_hours': store_info.get('opening_hours', {}).get('weekday_text', []),
                        'place_id': place['place_id']
                    })
                
                time.sleep(0.1)  # Rate limiting
        
        return stores
        
    except Exception as e:
        st.error(f"Error fetching location data: {str(e)}")
        return []

def analyze_competitors_with_locations(gemini_api_key: str, location: str, stores_data: List[Dict], detail_level: str):
    """Analyze competitors with real location data"""
    try:
        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_api_key,
            temperature=0.3,
            max_output_tokens=4096
        )
        
        # Format store data for analysis
        stores_text = ""
        for i, store in enumerate(stores_data, 1):
            price_level_text = {
                1: "Budget ($)",
                2: "Mid-range ($$)", 
                3: "Premium ($$$)",
                4: "Luxury ($$$$)"
            }.get(store['price_level'], "Unknown")
            
            stores_text += f"""
            {i}. **{store['name']}**
               - Address: {store['address']}
               - Rating: {store['rating']}/5
               - Price Level: {price_level_text}
               - Phone: {store['phone']}
               - Website: {store['website']}
               - Opening Hours: {', '.join(store['opening_hours'][:2]) if store['opening_hours'] else 'Not available'}
            """
        
        system_prompt = f"""
        You are a retail market research expert. Analyze the clothing store market in {location} using the following REAL competitor data:

        {stores_text}
        
        Provide a comprehensive analysis with these sections:
        
        ## Competitive Analysis: {location}
        
        ### 1. Competitor Overview
        Create a detailed table with:
        - Store Name
        - Full Address
        - Market Position (based on price level and rating)
        - Customer Rating
        - Contact Information
        - Estimated Target Demographic
        
        ### 2. Location Analysis
        - Geographic distribution of competitors
        - High-concentration areas
        - Underserved areas with opportunities
        - Accessibility analysis
        
        ### 3. Market Positioning Analysis
        - Price level distribution
        - Rating analysis
        - Market gaps identification
        
        ### 4. Strategic Recommendations
        - Optimal location suggestions
        - Pricing strategies based on competitor analysis
        - Market positioning opportunities
        - Competitive differentiation strategies
        
        ### 5. Executive Summary
        - Key findings from real data
        - Market opportunities
        - Recommended actions
        
        Detail Level: {detail_level}
        Use markdown formatting with tables. Base all analysis on the provided real data.
        """
        
        human_prompt = f"""
        Generate a {detail_level.lower()} competitor analysis for clothing stores in {location}.
        Use the real competitor data provided to give specific, actionable insights.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        # Get response
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

def to_latin1(text):
    # Remove all characters not in Latin-1
    return text.encode('latin1', errors='ignore').decode('latin1')

def generate_pdf_report(location, detail_level, stores, analysis_markdown):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, to_latin1("Clothing Store Competitor Analysis"), ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, to_latin1(f"Location: {location}"), ln=True)
    pdf.cell(0, 10, to_latin1(f"Detail Level: {detail_level}"), ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, to_latin1("Competitors:"), ln=True)
    pdf.set_font("Arial", '', 11)
    for i, store in enumerate(stores, 1):
        store_text = (
            f"{i}. {store['name']}\n"
            f"   Address: {store['address']}\n"
            f"   Rating: {store['rating']} / 5\n"
            f"   Price Level: {store['price_level']}\n"
            f"   Phone: {store['phone']}\n"
            f"   Website: {store['website']}\n"
            f"   Hours: {', '.join(store['opening_hours'][:2]) if store['opening_hours'] else 'Not available'}\n"
        )
        pdf.multi_cell(0, 8, to_latin1(store_text), border=0)
        pdf.ln(1)
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, to_latin1("AI-Generated Analysis:"), ln=True)
    pdf.set_font("Arial", '', 11)
    import re
    clean_text = re.sub(r'[#*`>\-]+', '', analysis_markdown)
    pdf.multi_cell(0, 8, to_latin1(clean_text), border=0)
    return pdf.output(dest='S').encode('latin1')


def main():
    st.title("👔 Clothing Store Competitor Intelligence")
    st.subheader("AI-powered market analysis with real location data")

    tab1, tab2 = st.tabs(["Competitors", "Generate Analysis"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.header("Configuration")
            location = st.text_input("📍 Location", "Saravanampatti, Coimbatore", key="location_input")
            radius = st.slider("Search Radius (meters)", 1000, 10000, 2000, key="radius_input")
            detail_level = st.selectbox("Detail Level", ["Summary", "Detailed", "Comprehensive"], key="detail_level_input")
            fetch_btn = st.button("🔍 Fetch Competitors", type="secondary", key="fetch_btn")
            if fetch_btn:
                with st.spinner("Fetching nearby clothing stores..."):
                    stores = get_nearby_clothing_stores(GOOGLE_PLACES_API_KEY, location, radius)
                    st.session_state.stores = stores
                    st.session_state.location = location
                    st.session_state.radius = radius
                    st.session_state.detail_level = detail_level
                    if stores:
                        st.success(f"Found {len(stores)} clothing stores!")
                    else:
                        st.warning("No clothing stores found in the area")
            # Show Generate Analysis button only if stores are fetched
            if hasattr(st.session_state, 'stores') and st.session_state.stores:
                generate_btn = st.button("📊 Generate Analysis", type="primary", key="generate_btn")
                if generate_btn:
                    with st.spinner("Analyzing competitors with AI..."):
                        report = analyze_competitors_with_locations(
                            GEMINI_API_KEY,
                            st.session_state.location,
                            st.session_state.stores,
                            st.session_state.detail_level
                        )
                        st.session_state.analysis_report = report
                        st.success("Analysis Complete! Go to the 'Generate Analysis' tab to view and download the report.")
        with col2:
            if hasattr(st.session_state, 'stores') and st.session_state.stores:
                st.header("📍 Found Competitors")
                for store in st.session_state.stores:
                    with st.expander(f"🏪 {store['name']} - Rating: {store['rating']}/5"):
                        st.write(f"**Address:** {store['address']}")
                        st.write(f"**Phone:** {store['phone']}")
                        st.write(f"**Website:** {store['website']}")
                        if store['opening_hours']:
                            st.write(f"**Hours:** {store['opening_hours'][0] if store['opening_hours'] else 'Not available'}")
            else:
                st.info("No competitors found yet. Please use the configuration to fetch competitors.")

    with tab2:
        st.header("Generate Analysis Report")
        if hasattr(st.session_state, 'analysis_report') and st.session_state.analysis_report:
            location = st.session_state.get('location', "Saravanampatti, Coimbatore")
            detail_level = st.session_state.get('detail_level', "Summary")
            report = st.session_state.analysis_report
            st.markdown(report)
            # Generate PDF
            pdf_bytes = generate_pdf_report(location, detail_level, st.session_state.stores, report)
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_bytes,
                file_name=f"competitor_analysis_{location.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        else:
            st.info("Please generate the analysis in the 'Competitors' tab first.")

if __name__ == "__main__":
    main()