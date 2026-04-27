import streamlit as st
import plotly.graph_objects as go
import librosa
import numpy as np
from audiorecorder import audiorecorder
import tempfile
import os

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

st.title("🧠 NeuroSense 2.0")
st.subheader("NEWS2 + Voice AI + Time Prediction")

# =========================
# 🎤 Voice Analysis (FIXED)
# =========================
def analyze_voice(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)

        if len(y) < 1000:
            return "Not Available"

        energy = np.mean(librosa.feature.rms(y=y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        if energy < 0.02:
            return "Fatigued"
        elif tempo < 80:
            return "Slow"
        else:
            return "Normal"

    except Exception as e:
        st.error(f"Voice analysis error: {e}")
        return "Not Available"

# =========================
# ⏱️ Time Prediction
# =========================
def predict_time(risk):
    if risk >= 80:
        return "5–15 min"
    elif risk >= 60:
        return "15–30 min"
    elif risk >= 40:
        return "30–60 min"
    else:
        return "Stable"

# =========================
# Layout
# =========================
col1, col2 = st.columns([1,1.2])

with col1:
    st.markdown("### 📊 Patient Input")

    rr = st.slider("Respiratory Rate", 8, 40, 18)
    spo2 = st.slider("SpO₂", 70, 100, 98)
    temp = st.slider("Temperature", 34.0, 41.0, 37.0)
    sbp = st.slider("BP", 70, 200, 120)
    hr = st.slider("Heart Rate", 40, 150, 85)

    avpu = st.selectbox("Consciousness", ["Alert", "Voice", "Pain", "Unresponsive"])
    context = st.selectbox("Context", ["Sepsis", "Cardiac", "Respiratory", "Anxiety"])
    behavior = st.selectbox("Behavior", ["Normal", "Confused", "Slow"])
    baseline = st.slider("Baseline HR", 60, 100, 80)

    st.markdown("---")
    st.markdown("### 🎤 Voice Input")

    voice_status = "Not Available"

    # 🎙️ تسجيل مباشر
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
    audio_file = st.file_uploader("Upload voice", type=["wav","mp3","m4a"])

    if audio_file:
        st.audio(audio_file)

        # حفظ مؤقت
        suffix = "." + audio_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name

        voice_status = analyze_voice(tmp_path)
        st.success(f"Detected Voice: {voice_status}")

# =========================
# NEWS2
# =========================
news2 = 0

if rr <= 8: news2 += 3
elif rr <= 11: news2 += 1
elif rr <= 20: news2 += 0
elif rr <= 24: news2 += 2
else: news2 += 3

if spo2 <= 91: news2 += 3
elif spo2 <= 93: news2 += 2
elif spo2 <= 95: news2 += 1

if temp <= 35: news2 += 3
elif temp <= 36: news2 += 1
elif temp <= 38: news2 += 0
elif temp <= 39: news2 += 1
else: news2 += 2

if sbp <= 90: news2 += 3
elif sbp <= 100: news2 += 2
elif sbp <= 110: news2 += 1

if hr <= 40: news2 += 3
elif hr <= 50: news2 += 1
elif hr <= 90: news2 += 0
elif hr <= 110: news2 += 1
elif hr <= 130: news2 += 2
else: news2 += 3

if avpu != "Alert":
    news2 += 3

# =========================
# Enhanced Risk
# =========================
risk = news2 * 10
reasons = []

if context == "Sepsis":
    risk += 15
    reasons.append("Sepsis context")

if voice_status == "Fatigued":
    risk += 10
    reasons.append("Voice fatigue")

elif voice_status == "Slow":
    risk += 8
    reasons.append("Slow speech")

if behavior != "Normal":
    risk += 10
    reasons.append("Abnormal behavior")

if hr > baseline + 15:
    risk += 5
    reasons.append("Above baseline HR")

risk = max(min(risk, 100), 0)

# ⏱️ Time
ttd = predict_time(risk)

# =========================
# OUTPUT
# =========================
with col2:
    st.markdown("### 📈 Results")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text': "Risk %"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.metric("NEWS2", news2)
    st.metric("⏱️ Time to Deterioration", ttd)

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
# Digital Twin
# =========================
st.markdown("### 🔮 Digital Twin")

colA, colB = st.columns(2)

with colA:
    st.error(f"No Intervention: {min(risk+20,100)}%")

with colB:
    st.success(f"Early Intervention: {max(risk-30,0)}%")

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("*NeuroSense 2.0 — Clean Final Version*")
