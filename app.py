import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model
model = joblib.load("new_model.joblib")
feature_names = model.feature_names_in_

st.set_page_config(page_title="Intrusion Detection", layout="centered")
st.title("🔐 Real-Time Intrusion Detection")
st.write("Enter network traffic features manually or simulate random values.")

# Simulated random values (approximate range [0, 1000], you can adjust this)
def generate_random_input():
    return {feature: np.round(np.random.uniform(0, 1000), 5) for feature in feature_names}

# State to track if random data should be used
use_random = st.button("🎲 Simulate Random Data")

# Create a prediction form
with st.form("prediction_form"):
    st.write("### Feature Input")

    # If simulate was clicked, use generated values
    random_input = generate_random_input() if use_random else {}
    input_data = {}

    for feature in feature_names:
        default_val = random_input.get(feature, 0.0)
        input_data[feature] = st.number_input(f"{feature}", value=default_val, format="%.5f")

    submitted = st.form_submit_button("Predict")

# Make prediction
if submitted:
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]

    # Handle label type (0/1 or string)
    if isinstance(prediction, (int, np.integer)):
        pred_label = "🚨 Attack" if prediction == 1 else "✅ Benign"
    else:
        pred_label = f"🚨 Attack" if prediction.lower() == "attack" else "✅ Benign"

    st.subheader("Prediction Result")
    st.success(pred_label)

