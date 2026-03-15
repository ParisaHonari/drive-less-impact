import streamlit as st
import pandas as pd
import requests

APP_URL = "https://parisahnr.com/drive-less-impact-calculator"

st.set_page_config(page_title="Drive Less Impact Calculator", layout="centered")
st.markdown("""
<style>

/* Page background */
.stApp {
    background-color: #F5F7FA;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}

/* Dropdown */
div[data-baseweb="select"] {
    background-color: white !important;
    border-radius: 8px !important;
    color: black !important;
}

/* Dropdown text */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Number input */
input {
    background-color: white !important;
    color: black !important;
}

/* Calculate button */
.stButton > button {
    background-color: #2E7D32;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 18px;
    border: none;
}

.stButton > button:hover {
    background-color: #1B5E20;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)
st.title("🚗 Drive Less Impact Calculator")
st.caption("Built by Parisa Honari | Data, AI & Sustainability")

st.write("See the environmental impact of your driving — and how much you save by skipping a trip.")




gas_url = "https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=2tKCHNwFTnG8eMy7MGT3RPFEBG4Sj7rIIdC2a23b&frequency=weekly&data%5B0%5D=value&facets%5Bproduct%5D%5B%5D=EPMR&facets%5Bduoarea%5D%5B%5D=NUS"

gas_response = requests.get(gas_url)
gas_data = gas_response.json()

gas_price = float(gas_data["response"]["data"][0]["value"]) if "response" in gas_data else 3.50

st.write(f"Current US gasoline price: **${gas_price:.2f} per gallon**")

# --- UI Inputs

vehicle_type = st.selectbox(
    "Vehicle Type",
    ["Gas Sedan", "Hybrid", "SUV", "Pickup Truck", "Electric Vehicle"]
)

year = st.number_input("Vehicle Year", min_value=1970, max_value=2025, value=2020)

distance = st.number_input("Miles driven", value=10)

# ---  MPG estimation based on vehicle type

if vehicle_type == "Gas Sedan":
    mpg = 30
elif vehicle_type == "Hybrid":
    mpg = 50
elif vehicle_type == "SUV":
    mpg = 22
elif vehicle_type == "Pickup Truck":
    mpg = 18
elif vehicle_type == "Electric Vehicle":
    mpg = 120  # MPGe equivalent

# --- Calculate
if st.button("Calculate Impact"):

    fuel_used = distance / mpg
    trip_cost = fuel_used * gas_price

    co2_per_gallon = 8887
    co2_kg = (fuel_used * co2_per_gallon) / 1000

    trees = co2_kg / 21

    st.subheader("Trip Impact")

    col1, col2 = st.columns(2)

    col1.metric("⛽ Fuel Used", f"{fuel_used:.2f} gallons")
    col1.metric("💸 Trip Cost", f"${trip_cost:.2f}")

    col2.metric("🌍 CO₂ Emitted", f"{co2_kg:.2f} kg")
    col2.metric("🌳 Trees Needed", f"{trees:.2f}")

    st.divider()

    st.subheader("💡 Work From Home Scenario")

    st.success(f"""
Told my boss I’m working from home today.

Apparently saving:
🌍 {co2_kg:.2f} kg CO₂
⛽ {fuel_used:.2f} gallons of gas
💵 ${trip_cost:.2f}

The planet approves.
""")
    post_text = f"""
    I just calculated my driving emissions using this tool 🌱

    Skipping {distance} miles saves:
    🌱 {co2_kg:.2f} kg CO₂
    ⛽ {fuel_used:.2f} gallons of gas
    💰 ${trip_cost:.2f}

Try it yourself:
{APP_URL}

#Sustainability #ClimateTech #DataScience
"""

    st.text_area("Copy this LinkedIn post:", post_text, height=180)
    share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={APP_URL}"
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={APP_URL}"
    tiktok_url = "https://www.tiktok.com/upload"

    st.markdown("### Share your impact 🌍")
    col1, col2, col3 = st.columns(3)
    
    with col1:
     st.markdown(
    f'<a href="{share_url}" target="_blank">'
    '<button style="background-color:#0077B5;color:white;padding:10px 20px;border:none;border-radius:5px;">'
    'Share on LinkedIn'
    '</button></a>',
    unsafe_allow_html=True)

    with col2:
     st.markdown(
    f'<a href="{facebook_url}" target="_blank">'
    '<button style="background-color:#1877F2;color:white;padding:10px 20px;border:none;border-radius:5px;margin-left:10px;">'
    'Share on Facebook'
    '</button></a>',
    unsafe_allow_html=True)

    with col3:
     st.markdown(
        f'<a href="{tiktok_url}" target="_blank">'
        '<button style="background-color:#000000;color:white;padding:10px 20px;border:none;border-radius:5px;">'
        'Share on TikTok'
        '</button></a>',
        unsafe_allow_html=True
    )
        



