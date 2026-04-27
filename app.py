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
    box-shadow: 0 3px 10px rgb…
[٩:٥١ ص, ٢٧‏/٤‏/٢٠٢٦] Mansour: import streamlit as st

st.set_page_config(page_title="NeuroSense 2.0", layout="wide")

st.title("🧠 NeuroSense 2.0")
st.subheader("Adaptive Clinical Intelligence System")

st.image("images/ai.png", use_container_width=True)

st.markdown("""
### 🚨 The Problem
Patients may appear stable but deteriorate suddenly.

### 💡 Our Solution
NeuroSense combines:
- Vital signs  
- Voice  
- Behavior  
- Context  

to predict deterioration early.

---

### 🔗 Navigate using the sidebar:
- Dashboard  
- Digital Twin  
- About  
"""
