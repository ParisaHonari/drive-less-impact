import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Drive Less Impact Calculator", layout="centered")

st.title("🚗 Drive Less Impact Calculator")
st.caption("Built by Parisa Honari | Data, AI & Sustainability")

st.write("See the environmental impact of your driving — and how much you save by skipping a trip.")

# --- Load EPA vehicle dataset
vehicles = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv")

# Extract make and model from vehicle name
vehicles["make"] = vehicles["name"].apply(lambda x: x.split()[0])
vehicles["model"] = vehicles["name"]

makes = sorted(vehicles["make"].dropna().unique() )

gas_url = "https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=2tKCHNwFTnG8eMy7MGT3RPFEBG4Sj7rIIdC2a23b&frequency=weekly&data%5B0%5D=value&facets%5Bproduct%5D%5B%5D=EPMR&facets%5Bduoarea%5D%5B%5D=NUS"

gas_response = requests.get(gas_url)
gas_data = gas_response.json()

gas_price = float(gas_data["response"]["data"][0]["value"]) if "response" in gas_data else 3.50

st.write(f"Current US gasoline price: **${gas_price:.2f} per gallon**")

# --- UI Inputs

make = st.selectbox("Vehicle Make", makes)

models = vehicles[vehicles["make"] == make]["model"].unique()
model = st.selectbox("Vehicle Model", models)

year = st.number_input("Vehicle Year", min_value=1970, max_value=2025, value=2020)

distance = st.number_input("Miles driven", value=10)

# --- MPG approximation (dataset doesn't have exact MPG so we estimate)
mpg = 25

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

    st.success(
        f"""
Told my boss I’m working from home today.

Apparently saving:
🌍 {co2_kg:.2f} kg CO₂  
⛽ {fuel_used:.2f} gallons of gas  
💰 ${trip_cost:.2f}

The planet approves. 🌎
"""
    )
