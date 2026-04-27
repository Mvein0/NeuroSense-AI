import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# =========================
# 🎨 UI STYLE
# =========================
st.markdown("""
<style>
body {background-color: #f4f7fb;}
.block-container {padding: 2rem;}
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 NeuroSense 2.0")
st.subheader("NEWS2 + Context-Aware AI")

col1, col2 = st.columns([1,1.2])

# =========================
# INPUT
# =========================
with col1:
    st.markdown("### 📊 Patient Input")

    rr = st.slider("Respiratory Rate", 8, 40, 18)
    spo2 = st.slider("Oxygen Saturation", 70, 100, 98)
    temp = st.slider("Temperature", 34.0, 41.0, 37.0)
    sbp = st.slider("Systolic BP", 70, 200, 120)
    hr = st.slider("Heart Rate", 40, 150, 85)

    avpu = st.selectbox("Consciousness", ["Alert", "Voice", "Pain", "Unresponsive"])

    voice = st.selectbox("Voice", ["Normal", "Fatigued", "Slow", "Not Available"])
    behavior = st.selectbox("Behavior", ["Normal", "Confused", "Slow"])

    context = st.selectbox("Context", ["Sepsis", "Cardiac", "Respiratory", "Anxiety"])

    baseline = st.slider("Baseline HR", 60, 100, 80)

# =========================
# 🧮 NEWS2 CALCULATION
# =========================
news2 = 0

# RR
if rr <= 8: news2 += 3
elif rr <= 11: news2 += 1
elif rr <= 20: news2 += 0
elif rr <= 24: news2 += 2
else: news2 += 3

# SpO2
if spo2 <= 91: news2 += 3
elif spo2 <= 93: news2 += 2
elif spo2 <= 95: news2 += 1

# Temp
if temp <= 35: news2 += 3
elif temp <= 36: news2 += 1
elif temp <= 38: news2 += 0
elif temp <= 39: news2 += 1
else: news2 += 2

# SBP
if sbp <= 90: news2 += 3
elif sbp <= 100: news2 += 2
elif sbp <= 110: news2 += 1

# HR
if hr <= 40: news2 += 3
elif hr <= 50: news2 += 1
elif hr <= 90: news2 += 0
elif hr <= 110: news2 += 1
elif hr <= 130: news2 += 2
else: news2 += 3

# AVPU
if avpu != "Alert":
    news2 += 3

# =========================
# 🔥 ENHANCED SCORE
# =========================
risk = news2 * 10

# Context
if context == "Sepsis":
    risk += 15
elif context == "Anxiety":
    risk -= 10

# Voice
if voice == "Fatigued":
    risk += 10
elif voice == "Slow":
    risk += 8

# Behavior
if behavior != "Normal":
    risk += 10

# Baseline
if hr > baseline + 15:
    risk += 5

risk = max(min(risk, 100), 0)

confidence = int(60 + risk * 0.3)

# =========================
# OUTPUT
# =========================
with col2:
    st.markdown("### 📈 Results")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text': "Risk %"},
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

    st.metric("NEWS2 Score", news2)

    if risk > 70:
        st.error("🔴 High Risk")
        rec = "Immediate intervention"
    elif risk > 40:
        st.warning("🟠 Moderate Risk")
        rec = "Close monitoring"
    else:
        st.success("🟢 Low Risk")
        rec = "Routine care"

    st.write(f"💡 Recommendation: {rec}")
    st.write(f"📊 Confidence: {confidence}%")

# =========================
# 🔮 DIGITAL TWIN
# =========================
st.markdown("### 🔮 Digital Twin Simulation")

colA, colB = st.columns(2)

with colA:
    st.error(f"❌ No Intervention: {min(risk+20,100)}%")

with colB:
    st.success(f"✅ Early Intervention: {max(risk-30,0)}%")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("*NeuroSense 2.0 — NEWS2 Enhanced • Context-Aware • Adaptive AI*")
