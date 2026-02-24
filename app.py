import streamlit as st
import pandas as pd
import pickle

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Customer Churn Predictor", layout="wide")

# -------------------------
# Load Model
# -------------------------
model = pickle.load(open("final_churn_model.pkl", "rb"))

# -------------------------
# Dark Theme Styling
# -------------------------
# 

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #0E1117;
}

/* Button Styling */
.stButton > button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    border: none;
    font-weight: 600;
    transition: 0.3s ease;
}

/* Hover Effect */
.stButton > button:hover {
    background-color: #028c94;
    color: white;
}

/* Active Click Effect */
.stButton > button:active {
    background-color: #016d73;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Title
# -------------------------
st.title("📊 Customer Churn Prediction Dashboard")
st.write("Predict customer churn risk using Machine Learning.")

# -------------------------
# Layout Columns
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Customer Profile")
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.number_input("Tenure (Months)", min_value=0)

with col2:
    st.subheader("📦 Service Details")
    phone = st.selectbox("Phone Service", ["Yes", "No"])
    multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    if internet == "No":
        security = backup = device = tech = tv = movies = "No internet service"
        st.info("No internet service selected — related services auto-disabled.")
    else:
        security = st.selectbox("Online Security", ["Yes", "No"])
        backup = st.selectbox("Online Backup", ["Yes", "No"])
        device = st.selectbox("Device Protection", ["Yes", "No"])
        tech = st.selectbox("Tech Support", ["Yes", "No"])
        tv = st.selectbox("Streaming TV", ["Yes", "No"])
        movies = st.selectbox("Streaming Movies", ["Yes", "No"])

# -------------------------
# Contract Section
# -------------------------
st.subheader("💳 Contract & Billing")
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
payment = st.selectbox("Payment Method", [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)"
])

monthly = st.number_input("Monthly Charges", min_value=0.0)

# Auto-calculate TotalCharges
total = tenure * monthly

# -------------------------
# Risk Score Logic
# -------------------------
def calculate_risk_score():
    score = 0
    
    if contract == "Month-to-month":
        score += 1
    if payment == "Electronic check":
        score += 1
    if internet == "Fiber optic":
        score += 1
    if tenure <= 12:
        score += 1
    if monthly > 70:
        score += 1
        
    return score

# -------------------------
# Prediction Button
# -------------------------
if st.button("Predict Churn Risk"):

    input_df = pd.DataFrame([{
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    risk_score = calculate_risk_score()

    if risk_score <= 1:
        risk_category = "Low"
    elif risk_score <= 3:
        risk_category = "Medium"
    else:
        risk_category = "High"

    # -------------------------
    # Display Results
    # -------------------------
    st.subheader("🔮 Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk of Churn ({probability:.2%})")
    else:
        st.success(f"✅ Low Risk of Churn ({probability:.2%})")

    st.write("### 📊 Rule-Based Risk Score")
    st.write(f"Score: {risk_score} / 5")
    st.write(f"Risk Category: **{risk_category}**")

    st.write("### 💡 Recommendation")
    if risk_category == "High":
        st.warning("Offer long-term contract discounts and promote auto-payment methods.")
    elif risk_category == "Medium":
        st.info("Engage customer with personalized offers and service improvements.")
    else:
        st.success("Customer appears stable. Maintain satisfaction with loyalty benefits.")