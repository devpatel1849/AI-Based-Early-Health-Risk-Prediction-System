import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Risk Predictor",
    page_icon="🩺",
    layout="wide"
)

# ---------------- LOAD BACKGROUND IMAGE ----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

doctor_bg = get_base64_image("doctor.png")

# ---------------- CSS WITH DOCTOR THEME ----------------
st.markdown(f"""
<style>
/* Background image with quality boost */
.stApp {{
    background-image: url("data:image/jpg;base64,{doctor_bg}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;

    /* Quality improvement */
    filter: saturate(1.2) contrast(1.15) brightness(1.08);
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;

    color: white;
}}

/* Soft dark overlay (lighter than before) */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);  /* reduced darkness */
    z-index: -1;
}}

/* Headings */
h1, h2, h3 {{
    color: #f1f9ff;
}}

/* Cards */
.card {{
    background-color: rgba(255, 255, 255, 0.97);
    color: black;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    margin-bottom: 15px;
}}

/* Risk colors */
.low {{color: #27ae60; font-size: 22px; font-weight: bold;}}
.medium {{color: #f39c12; font-size: 22px; font-weight: bold;}}
.high {{color: #e74c3c; font-size: 22px; font-weight: bold;}}

/* Buttons */
.stButton>button {{
    background: linear-gradient(135deg, #1abc9c, #16a085);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-size: 16px;
    border: none;
}}
.stButton>button:hover {{
    background: linear-gradient(135deg, #16a085, #149174);
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🩺 AI-Based Early Health Risk Prediction System")
st.caption("Preventive Healthcare using AI | AI For Good Hackathon")
st.divider()

# ---------------- LAYOUT ----------------
left, right = st.columns([1.2, 1])

# ---------------- USER INPUT ----------------
with left:
    st.subheader("👤 User Health Information")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    age = st.slider("Age (Years)", 10, 90, 35)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 30, 150, 70)
    height = st.number_input("Height (cm)", 120, 210, 170)
    bp = st.slider("Blood Pressure – Systolic", 80, 200, 125)
    sugar = st.slider("Blood Sugar Level (mg/dL)", 70, 300, 115)
    activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
    smoking = st.selectbox("Smoking Habit", ["No", "Yes"])

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- AI LOGIC ----------------
bmi = round(weight / ((height / 100) ** 2), 2)

risk_score = 0
if bmi > 25: risk_score += 1
if bp > 140: risk_score += 1
if sugar > 140: risk_score += 1
if age > 45: risk_score += 1
if activity == "Low": risk_score += 1
if smoking == "Yes": risk_score += 1

# ---------------- RESULT ----------------
with right:
    st.subheader("🧠 AI Health Assessment Result")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.write(f"**BMI:** {bmi}")
    st.write(f"**BMI Status:** {'Overweight' if bmi > 25 else 'Normal'}")

    if risk_score <= 2:
        st.markdown("<p class='low'>Risk Level: LOW</p>", unsafe_allow_html=True)
        condition = "You are currently at low health risk."
        advice = "No immediate doctor visit required. Maintain healthy lifestyle and annual checkups."
    elif risk_score <= 4:
        st.markdown("<p class='medium'>Risk Level: MEDIUM</p>", unsafe_allow_html=True)
        condition = "Moderate health risk detected."
        advice = "Doctor consultation is advised within the next 2–3 weeks."
    else:
        st.markdown("<p class='high'>Risk Level: HIGH</p>", unsafe_allow_html=True)
        condition = "High health risk detected."
        advice = "Immediate doctor consultation is strongly recommended."

    st.write(f"**Condition Summary:** {condition}")
    st.write(f"**Medical Guidance:** {advice}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LIVE GRAPH ----------------
st.subheader("📊 Health Risk Factor Analysis (Live)")
factors = ["BMI", "Blood Pressure", "Sugar", "Age", "Lifestyle"]
values = [bmi, bp/2, sugar/2, age, 40 if activity == "Low" else 20]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(factors, values)
ax.set_ylabel("Relative Risk Impact")
ax.set_ylim(0, max(values) + 20)
st.pyplot(fig)

# ---------------- ACTION BUTTONS ----------------
st.divider()
st.subheader("🛠️ Actions")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🔄 Recheck Health Risk"):
        st.rerun()

with c2:
    if st.button("🩺 Doctor Visit Advice"):
        if risk_score <= 2:
            st.success("✅ No immediate doctor visit needed.")
        elif risk_score <= 4:
            st.warning("⏳ Visit doctor within 2–3 weeks.")
        else:
            st.error("🚨 Meet doctor immediately.")

with c3:
    report = f"""
AI HEALTH RISK SUMMARY REPORT

Age: {age}
Gender: {gender}
BMI: {bmi}
Blood Pressure: {bp}
Sugar Level: {sugar}
Physical Activity: {activity}
Smoking: {smoking}

Final Risk Level:
{"LOW" if risk_score<=2 else "MEDIUM" if risk_score<=4 else "HIGH"}

Note: This report is for awareness only.
"""
    st.download_button("📄 Download Health Report", report, file_name="health_risk_report.txt")
    
st.caption("AI For Good Hackathon | Doctor-Themed Preventive Healthcare Prototype")
