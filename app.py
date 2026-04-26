import streamlit as st

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# 🟦 Title

st.title("🧠 NeuroSense 2.0")

st.subheader("Adaptive Clinical Intelligence System")

# =========================

# 🧾 INPUT

# =========================

col1, col2 = st.columns(2)

with col1:

    st.header("📊 Patient Input")

    hr = st.slider("Heart Rate (HR)", 50, 150, 85)

    rr = st.slider("Respiratory Rate (RR)", 10, 40, 18)

    bp = st.slider("Blood Pressure (BP)", 80, 180, 120)

    voice = st.selectbox("🎤 Voice Condition", ["Normal", "Fatigued", "Slow"])

    behavior = st.selectbox("🧠 Behavior", ["Normal", "Confused", "Slow response"])

    context = st.selectbox("📌 Clinical Context", ["Sepsis", "Chest Pain", "Anxiety"])

    baseline_hr = st.slider("Baseline HR (Personalized)", 60, 100, 80)

# =========================

# 🧠 AI ENGINE

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

    reasons.append("Abnormal behavior")

if context == "Sepsis":

    risk += 15

elif context == "Anxiety":

    risk -= 10

if hr > baseline_hr + 15:

    risk += 10

    reasons.append("Above personal baseline")

risk = max(min(risk, 100), 0)

# =========================

# 📊 OUTPUT

# =========================

with col2:

    st.header("📈 AI Output")

    st.metric("Risk Score", f"{risk}%")

    st.progress(risk)

    if risk > 70:

        st.error("🔴 HIGH RISK")

        recommendation = "Immediate intervention"

    elif risk > 40:

        st.warning("🟠 Moderate Risk")

        recommendation = "Close monitoring"

    else:

        st.success("🟢 Low Risk")

        recommendation = "Routine care"

    st.write(f"💡 Recommendation: *{recommendation}*")

    if risk > 70:

        time_est = "30–45 minutes"

    elif risk > 40:

        time_est = "1–2 hours"

    else:

        time_est = "Stable"

    st.write(f"⏱️ Time to deterioration: {time_est}")

    confidence = 60 + (risk * 0.3)

    st.write(f"📊 Confidence: {int(confidence)}%")

    st.write("🧾 Explanation:")

    st.write(", ".join(reasons) if reasons else "No significant risk factors")

# =========================

# 📊 Breakdown

# =========================

st.header("📊 Risk Breakdown")

chart_data = {

    "HR": 25 if hr > 100 else 5,

    "RR": 25 if rr > 22 else 5,

    "Voice": 20 if voice != "Normal" else 5,

    "Behavior": 20 if behavior != "Normal" else 5,

}

st.bar_chart(chart_data)

# =========================

# 🔮 DIGITAL TWIN

# =========================

st.header("🔮 Digital Twin Simulation")

colA, colB = st.columns(2)

with colA:

    st.subheader("❌ No Intervention")

    st.error(f"Predicted Risk: {min(risk + 20, 100)}%")

with colB:

    st.subheader("✅ Early Intervention")

    st.success(f"Predicted Risk: {max(risk - 30, 0)}%")

# =========================

# 🎤 Voice (Prototype)

# =========================

st.header("🎤 Voice Input (Prototype)")

audio = st.file_uploader("Upload voice sample", type=["wav", "mp3"])

if audio:

    st.audio(audio)

    st.info("Voice features extracted: pauses, speed, fatigue")

st.markdown("---")

st.caption("⚠️ Prototype only. Not for real clinical use.")
