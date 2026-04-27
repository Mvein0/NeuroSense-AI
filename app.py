import streamlit as st
import plotly.graph_objects as go
import librosa
import numpy as np
from audiorecorder import audiorecorder
import tempfile

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

st.title("🧠 NeuroSense 2.0")
st.subheader("Research-Level: NEWS2 + Voice AI + Survival Analysis")

# =========================
# 🎤 Voice Analysis
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
# 🧠 Survival Model
# =========================
def compute_hazard(hr, rr, spo2, temp, voice_status, context):
    beta_hr = 0.02
    beta_rr = 0.05
    beta_spo2 = -0.04
    beta_temp = 0.03

    voice_factor = 0.2 if voice_status == "Fatigued" else 0
    context_factor = 0.3 if context == "Sepsis" else 0

    linear_pred = (
        beta_hr * hr +
        beta_rr * rr +
        beta_spo2 * spo2 +
        beta_temp * temp +
        voice_factor +
        context_factor
    )

    return np.exp(linear_pred)

def survival_curve(hazard):
    times = np.linspace(0, 120, 50)
    survival = np.exp(-hazard * times / 100)
    return times, survival

def predict_ttd(times, survival):
    for t, s in zip(times, survival):
        if s < 0.5:
            return int(t)
    return ">120"

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

    # تسجيل مباشر
    audio_rec = audiorecorder("Start Recording", "Stop Recording")
    if len(audio_rec) > 0:
        audio_bytes = audio_rec.export().read()
        st.audio(audio_bytes)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            voice_status = analyze_voice(tmp.name)

        st.success(f"Detected Voice: {voice_status}")

    # رفع ملف
    audio_file = st.file_uploader("Upload voice", type=["wav","mp3"])
    if audio_file:
        st.audio(audio_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            voice_status = analyze_voice(tmp.name)

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

if behavior != "Normal":
    risk += 10
    reasons.append("Abnormal behavior")

if hr > baseline + 15:
    risk += 5
    reasons.append("Above baseline HR")

risk = max(min(risk, 100), 0)

# =========================
# 🧠 Survival Analysis
# =========================
hazard = compute_hazard(hr, rr, spo2, temp, voice_status, context)
times, survival = survival_curve(hazard)
ttd = predict_ttd(times, survival)

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
    st.metric("⏱️ Time to Deterioration", f"{ttd} min")

    if risk > 70:
        st.error("🔴 High Risk")
    elif risk > 40:
        st.warning("🟠 Moderate Risk")
    else:
        st.success("🟢 Low Risk")

    st.markdown("### 🧾 Explanation")
    for r in reasons:
        st.write(f"- {r}")

    st.write(f"Hazard Score: {round(hazard,2)}")

# =========================
# 📊 Survival Curve
# =========================
st.markdown("### 📊 Survival Curve")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=times, y=survival, mode='lines'))
fig2.update_layout(
    xaxis_title="Time (minutes)",
    yaxis_title="Survival Probability"
)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# 🔮 Digital Twin
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
st.markdown("*NeuroSense 2.0 — Research-Level Clinical AI*")
