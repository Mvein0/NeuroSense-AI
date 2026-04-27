import streamlit as st

st.title("🔮 Digital Twin Simulation")

risk = st.slider("Base Risk", 0, 100, 60)

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ No Intervention")
    st.error(f"Risk: {min(risk+20,100)}%")

with col2:
    st.subheader("✅ Early Intervention")
    st.success(f"Risk: {max(risk-30,0)}%")

st.markdown("""
### 💡 Insight
The system simulates outcomes before decisions are made.
""")
