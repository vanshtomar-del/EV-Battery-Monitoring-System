import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="EV Battery Monitoring Dashboard",
    layout="wide"
)

st.title("⚡ EV Battery Monitoring Dashboard")
st.sidebar.title("Control Panel")
st.sidebar.write("Live Battery Monitoring")

# Auto Refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# -------------------- FIREBASE --------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")

    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://ev-battery-monitoring-fba3e-default-rtdb.firebaseio.com/"
        }
    )

# -------------------- READ DATA --------------------
def get_data():
    ref = db.reference("battery")
    return ref.get()

battery = get_data()

if battery is None:
    st.error("No data found in Firebase!")
    st.stop()

voltage = battery.get("voltage", 0)
current = battery.get("current", 0)
temperature = battery.get("temperature", 0)
soc = battery.get("soc", 0)
power = battery.get("power", 0)
status = battery.get("status", "Unknown")

# -------------------- ALERT LOGIC --------------------
if temperature > 40:
    status = "🔴 High Temperature"
elif voltage < 3.3:
    status = "🟡 Low Battery"
elif current > 2.5:
    status = "🟠 High Current"
else:
    status = "🟢 Normal"

# -------------------- METRICS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⚡ Voltage", f"{voltage} V")

with col2:
    st.metric("🔌 Current", f"{current} A")

with col3:
    st.metric("🌡 Temperature", f"{temperature} °C")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("🔋 SoC", f"{soc}%")

with col5:
    st.metric("⚙ Power", f"{power} W")

with col6:
    st.metric("Status", status)

# -------------------- HISTORY --------------------
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=[
            "Voltage",
            "Current",
            "Temperature",
            "Power",
            "SoC"
        ]
    )

new_data = pd.DataFrame({
    "Voltage": [voltage],
    "Current": [current],
    "Temperature": [temperature],
    "Power": [power],
    "SoC": [soc]
})

st.session_state.history = pd.concat(
    [st.session_state.history, new_data],
    ignore_index=True
)

# Keep only latest 20 readings
st.session_state.history = st.session_state.history.tail(20)

df = st.session_state.history

# -------------------- CHARTS --------------------
st.subheader("⚡ Voltage Trend")
fig = px.line(df, y="Voltage", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔌 Current Trend")
fig = px.line(df, y="Current", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🌡 Temperature Trend")
fig = px.line(df, y="Temperature", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("⚙ Power Trend")
fig = px.line(df, y="Power", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔋 SoC Trend")
fig = px.line(df, y="SoC", markers=True)
st.plotly_chart(fig, use_container_width=True)