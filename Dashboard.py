import streamlit as st
import plotly.graph_objects as go

st.title("📊 Clinical Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Patient Input")

    hr = st.slider("Heart Rate", 50, 150, 85)
    rr = st.slider("Respiratory Rate", 10, 40, 18)
    voice = st.selectbox("Voice", ["Normal", "Fatigued", "Slow", "Not Available"])
    behavior = st.selectbox("Behavior", ["Normal", "Confused", "Slow"])

with col2:
    st.image("images/patient.png", use_container_width=True)

# AI Logic
risk = 0

if hr > 100:
    risk += 25
if rr > 22:
    risk += 25
if voice != "Normal":
    risk += 20
if behavior != "Normal":
    risk += 20

risk = min(risk, 100)

# Gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk,
    title={'text': "Risk Level"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#4A90E2"},
        'steps': [
            {'range': [0, 40], 'color': "#d4edda"},
            {'range': [40, 70], 'color': "#fff3cd"},
            {'range': [70, 100], 'color': "#f8d7da"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

if risk > 70:
    st.error("🔴 High Risk")
elif risk > 40:
    st.warning("🟠 Moderate Risk")
else:
    st.success("🟢 Low Risk")
