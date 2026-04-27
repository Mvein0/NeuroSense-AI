import streamlit as st

# =========================
# 🎨 PAGE CONFIG
# =========================
st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# =========================
# 🎨 CUSTOM CSS (Light UI)
# =========================
st.markdown("""
<style>
body {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}
.title {
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
}
.subtitle {
    color: #7f8c8d;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🟦 HEADER
# =========================
st.markdown('<div class="title">🧠 NeuroSense 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Adaptive Clinical Intelligence Dashboard</div>', unsafe_allow_html=True)

# =========================
# 🧾 INPUT SECTION
# =========================
col1, col2 = st.columns([1,1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Patient Input")

    hr = st.slider("Heart Rate (HR)", 50, 150, 85)
    rr = st.slider("Respiratory Rate (RR)", 10, 40, 18)
    bp = st.slider("Blood Pressure (BP)", 80, 180, 120)

    voice = st.selectbox("🎤 Voice", ["Normal", "Fatigued", "Slow", "Not Available"])
    behavior = st.selectbox("🧠 Behavior", ["Normal", "Confused", "Slow response"])

    context = st.selectbox("📌 Clinical Context", ["Sepsis", "Chest Pain", "Anxiety"])
    baseline = st.slider("👤 Baseline HR", 60, 100, 80)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🧠 AI LOGIC
# =========================
risk = 0
reasons = []

if hr > 100:
    risk += 25
    reasons.append("High HR")

if rr > 22:
    risk += 25
    reasons.append("High RR")

if voice == "Fatigued":
    risk += 20
    reasons.append("Voice fatigue")

if voice == "Slow":
    risk += 15
    reasons.append("Slow speech")

if behavior != "Normal":
    risk += 20
    reasons.append("Behavior abnormal")

if context == "Sepsis":
    risk += 15
elif context == "Anxiety":
    risk -= 10

if hr > baseline + 15:
    risk += 10
    reasons.append("Above baseline")

if voice == "Not Available":
    risk += 5
    reasons.append("Voice unavailable → relying on vitals")

risk = max(min(risk, 100), 0)

confidence = int(60 + risk * 0.3)

# =========================
# 📊 OUTPUT SECTION
# =========================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 AI Output")

    st.metric("Risk Score", f"{risk}%")
    st.progress(risk)

    if risk > 70:
        st.error("🔴 HIGH RISK")
        rec = "Immediate intervention"
    elif risk > 40:
        st.warning("🟠 Moderate Risk")
        rec = "Close monitoring"
    else:
        st.success("🟢 Low Risk")
        rec = "Routine care"

    st.write(f"💡 Recommendation: *{rec}*")

    # Time
    if risk > 70:
        time_est = "30–45 min"
    elif risk > 40:
        time_est = "1–2 hours"
    else:
        time_est = "Stable"

    st.write(f"⏱️ Time to deterioration: {time_est}")
    st.write(f"📊 Confidence: {confidence}%")

    st.markdown("*🧾 Explanation:*")
    st.write(", ".join(reasons) if reasons else "No risk factors")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 📊 CHART
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Risk Breakdown")

data = {
    "HR": 25 if hr > 100 else 5,
    "RR": 25 if rr > 22 else 5,
    "Voice": 20 if voice not in ["Normal","Not Available"] else 5,
    "Behavior": 20 if behavior != "Normal" else 5
}

st.bar_chart(data)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🔮 DIGITAL TWIN
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔮 Digital Twin Simulation")

colA, colB = st.columns(2)

with colA:
    st.error(f"❌ No Intervention: {min(risk+20,100)}%")

with colB:
    st.success(f"✅ Early Intervention: {max(risk-30,0)}%")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🎤 VOICE SECTION
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎤 Voice Input")

audio = st.file_uploader("Upload voice sample", type=["wav","mp3"])
if audio:
    st.audio(audio)
    st.info("Voice features extracted")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("*NeuroSense 2.0 — Understand • Simulate • Prevent*")
