import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

# =========================
# 🎨 CSS (Light Clean UI)
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}
.block-container {
    padding: 2rem;
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
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 HEADER
# =========================
st.markdown('<div class="title">🧠 NeuroSense 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Adaptive Clinical Intelligence System</div>', unsafe_allow_html=True)

# =========================
# 🖼️ IMAGE (اختياري)
# =========================
try:
    st.image("images/ai.png", use_container_width=True)
except:
    st.info("ضع صورة ai.png داخل مجلد images لإظهار الصورة")

# =========================
# 📄 MAIN CONTENT
# =========================
st.markdown("""
<div class="card">

<h3>🚨 The Problem</h3>
Patients may appear stable but suddenly deteriorate without clear warning.

<br>

<h3>💡 Our Solution</h3>
NeuroSense integrates:
<ul>
<li>Vital Signs</li>
<li>Voice Analysis</li>
<li>Behavior Monitoring</li>
<li>Clinical Context</li>
</ul>

to predict deterioration early.

<br>

<h3>🔮 Key Innovation</h3>
<ul>
<li>Adaptive AI (handles missing data)</li>
<li>Context-aware decision making</li>
<li>Digital Twin simulation</li>
<li>Explainable outputs</li>
</ul>

</div>
""", unsafe_allow_html=True)

# =========================
# 📌 NAVIGATION GUIDE
# =========================
st.markdown("""
### 📍 Navigate from the sidebar:
- 📊 Dashboard  
- 🔮 Digital Twin  
- ℹ️ About  

---
""")

# =========================
# 🏁 FOOTER
# =========================
st.markdown("*NeuroSense 2.0 — Understand • Simulate • Prevent*")
