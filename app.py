import streamlit as st
import plotly.graph_objects as go
import librosa
import numpy as np
from audiorecorder import audiorecorder
import tempfile

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# =========================
# 🎨 UI
# =========================
st.markdown("""
<style>
body {background-color: #f4f7fb;}
.block-container {padding: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 NeuroSense 2.0")
st.subheader("Multimodal adaptive AI")

# =========================
# 🎤 VOICE ANALYSIS FUNCTION
# =========================
def analyze_voice(audio_input):
    try:
        y, sr = librosa.load(audio_input, sr=None)

        energy = np.mean(librosa.feature.rms(y=y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        if energy < 0.02:
            return "Fatigued"
        elif tempo < 80:
            return "Slow"
        else:
            return "Normal"
    except:
        return "Not Available"

# =========================
# LAYOUT
# =========================
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

    context = st.selectbox("Context", ["Sepsis", "Cardiac", "Respiratory", "Anxiety"])
    behavior = st.selectbox("Behavior", ["Normal", "Confused", "Slow"])

    baseline = st.slider("Baseline HR", 60, 100, 80)

    st.markdown("---")
    st.markdown("### 🎤 Voice Input")

    voice_status = "Not Available"

    # 🎙️ تسجيل مباشر
    st.markdown("#### 🎙️ Record Voice")
    audio_rec = audiorecorder("Start Recording", "Stop Recording")

    if len(audio_rec) > 0:
        audio_bytes = audio_rec.export().read()
        st.audio(audio_bytes)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        voice_status = analyze_voice(tmp_path)
        st.success(f"Detected Voice: {voice_status}")

    # 📁 رفع ملف
    st.markdown("#### 📁 Or Upload Voice")
    audio_file = st.file_uploader("Upload voice", type=["wav","mp3"])

    if audio_file:
        st.audio(audio_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name

        voice_status = analyze_voice(tmp_path)
        st.success(f"Detected Voice: {voice_status}")

# =========================
# NEWS2
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
# ENHANCED SCORE
# =========================
risk = news2 * 10
reasons = []

# Context
if context == "Sepsis":
    risk += 15
    reasons.append("Sepsis context")
elif context == "Anxiety":
    risk -= 10
    reasons.append("Anxiety context")

# Voice
if voice_status == "Fatigued":
    risk += 10
    reasons.append("Voice fatigue detected")
elif voice_status == "Slow":
    risk += 8
    reasons.append("Slow speech detected")

# Behavior
if behavior != "Normal":
    risk += 10
    reasons.append("Abnormal behavior")

# Baseline
if hr > baseline + 15:
    risk += 5
    reasons.append("Above baseline HR")

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

    st.markdown("### 🧾 Explanation")
    if reasons:
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("No major contributing factors")

# =========================
# DIGITAL TWIN
# =========================
st.markdown("### 🔮 Digital Twin")

colA, colB = st.columns(2)

with colA:
    st.error(f"No Intervention: {min(risk+20,100)}%")

with colB:
    st.success(f"Early Intervention: {max(risk-30,0)}%")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("*NeuroSense 2.0 — Live Voice + NEWS2 + Context-Aware AI*")
