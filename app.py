import streamlit as st
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# =========================
# 🎨 ADVANCED CSS
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}

.block-container {
    padding: 2rem;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

.title {
    font-size: 34px;
    font-weight: 700;
    color: #1f2d3d;
}

.subtitle {
    color: #6b7c93;
    margin-bottom: 25px;
}

.small-card {
    background: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🧠 NeuroSense 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Adaptive Clinical Intelligence Dashboard</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
left, right = st.columns([1,1.2])

# =========================
# INPUT CARD
# =========================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Patient Input")

    hr = st.slider("Heart Rate", 50, 150, 85)
    rr = st.slider("Respiratory Rate", 10, 40, 18)
    bp = st.slider("Blood Pressure", 80, 180, 120)

    voice = st.selectbox("Voice", ["Normal", "Fatigued", "Slow", "Not Available"])
    behavior = st.selectbox("Behavior", ["Normal", "Confused", "Slow response"])
    context = st.selectbox("Context", ["Sepsis", "Chest Pain", "Anxiety"])

    baseline = st.slider("Baseline HR", 60, 100, 80)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AI LOGIC
# =========================
risk = 0
reasons = []

if hr > 100:
    risk += 25; reasons.append("High HR")
if rr > 22:
    risk += 25; reasons.append("High RR")
if voice == "Fatigued":
    risk += 20; reasons.append("Voice fatigue")
if voice == "Slow":
    risk += 15; reasons.append("Slow speech")
if behavior != "Normal":
    risk += 20; reasons.append("Abnormal behavior")
if context == "Sepsis":
    risk += 15
elif context == "Anxiety":
    risk -= 10
if hr > baseline + 15:
    risk += 10; reasons.append("Above baseline")
if voice == "Not Available":
    reasons.append("Voice missing → relying on vitals")

risk = max(min(risk, 100), 0)
confidence = int(60 + risk * 0.3)

# =========================
# OUTPUT UI
# =========================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 AI Risk Score")

    # 🎯 Gauge Chart
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
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Status
    if risk > 70:
        st.error("🔴 High Risk")
        rec = "Immediate intervention"
    elif risk > 40:
        st.warning("🟠 Moderate Risk")
        rec = "Close monitoring"
    else:
        st.success("🟢 Low Risk")
        rec = "Routine care"

    st.write(f"💡 *Recommendation:* {rec}")
    st.write(f"📊 *Confidence:* {confidence}%")

    st.markdown("*🧾 Explanation*")
    st.write(", ".join(reasons) if reasons else "No risk factors")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DIGITAL TWIN
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔮 Digital Twin Simulation")

col1, col2 = st.columns(2)

with col1:
    st.metric("No Intervention", f"{min(risk+20,100)}%")

with col2:
    st.metric("Early Intervention", f"{max(risk-30,0)}%")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("*NeuroSense 2.0 — Understand • Simulate • Prevent*")
