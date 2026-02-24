import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"   # your API

st.title("💡 Insurance Charges Predictor")
st.markdown("Fill in the details to get the predicted insurance charges.")

# --- INPUTS ---

age = st.number_input("Age", min_value=1, max_value=119, value=30)

sex = st.selectbox("Sex", ["male", "female"])

bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)

children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)

smoker = st.selectbox("Smoker?", ["yes", "no"])

region = st.selectbox(
    "Region",
    ["northeast", "northwest", "southeast", "southwest"]
)

# --- BUTTON ---
if st.button("Predict Insurance Charge"):

    input_data = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }

    st.write("📤 Sending data to API:", input_data)

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200:
            st.success(
                f"💰 Predicted Insurance Charge: **$ {round(result['predicted_charges'], 2)}**"
            )
        else:
            st.error("❌ API returned an error")
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server.")