import streamlit as st
import joblib
import numpy as np
import pandas as pd
import json

# --- Load model and metadata ---
model = joblib.load("new_model.joblib")
feature_names = model.feature_names_in_

with open("feature_ranges.json", "r") as f:
    feature_ranges = json.load(f)

# --- Dark mode CSS ---
dark_mode_css = """
<style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #1f2937;
        color: #e0e0e0;
    }
    .stSlider>div>div>input {
        background-color: #1e293b;
        color: #e0e0e0;
    }
    .css-1d391kg {
        background-color: #1f2937 !important;
    }
</style>
"""

light_mode_css = """
<style>
    body {
        background-color: white;
        color: black;
    }
    .stButton>button {
        background-color: #f0f0f0;
        color: black;
    }
    .stSlider>div>div>input {
        background-color: white;
        color: black;
    }
    .css-1d391kg {
        background-color: white !important;
    }
</style>
"""

st.set_page_config(page_title="🛡️ Real-Time Intrusion Detection", layout="wide")
st.title("🛡️ Real-Time Intrusion Detection System")
st.caption("Monitor simulated network traffic and predict whether it’s benign or an attack.")

# --- Dark mode toggle ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("Toggle Dark Mode 🌙", on_click=toggle_dark_mode)

if st.session_state.dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

st.markdown("---")

# --- Initialize session state ---
for feature in feature_names:
    if feature not in st.session_state:
        low, high = feature_ranges.get(feature, (0, 1))
        st.session_state[feature] = round((low + high) / 2, 5)

# --- Function to simulate realistic input ---
def generate_random_input():
    for feature in feature_names:
        low, high = feature_ranges.get(feature, (0, 1))
        st.session_state[feature] = round(np.random.uniform(low, high), 5)

# --- Simulation Button ---
st.markdown("### 🔧 Input Options")
col_sim, _ = st.columns([1, 4])
with col_sim:
    if st.button("🎲 Simulate Realistic Random Data"):
        generate_random_input()
        st.success("Random values generated.")

# --- Input Form with Sliders ---
with st.form("prediction_form"):
    st.markdown("### ✍️ Feature Input")
    input_data = {}

    # Split features into two columns
    left_col, right_col = st.columns(2)

    for i, feature in enumerate(feature_names):
        low, high = feature_ranges.get(feature, (0, 1))
        default_val = st.session_state[feature]

        # Set step size for slider to a sensible small fraction of range
        step = (high - low) / 1000 if (high - low) > 0 else 0.01

        if i % 2 == 0:
            input_val = left_col.slider(
                label=feature,
                min_value=float(low),
                max_value=float(high),
                value=float(default_val),
                step=step,
                format="%.5f"
            )
        else:
            input_val = right_col.slider(
                label=feature,
                min_value=float(low),
                max_value=float(high),
                value=float(default_val),
                step=step,
                format="%.5f"
            )

        input_data[feature] = input_val
        st.session_state[feature] = input_val

    submitted = st.form_submit_button("🚀 Predict")

# --- Prediction Section ---
if submitted:
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]  # [prob_benign, prob_attack]

    # Determine label and confidence
    if isinstance(prediction, (int, np.integer)):
        pred_label = "🚨 **Attack**" if prediction == 1 else "✅ **Benign**"
    else:
        pred_label = "🚨 **Attack**" if str(prediction).lower() == "attack" else "✅ **Benign**"

    confidence = max(prediction_proba)
    confidence_pct = round(confidence * 100, 2)

    # Display Result
    st.markdown("---")
    st.markdown("## 🧠 Prediction Result")
    if "attack" in pred_label.lower():
        st.error(f"{pred_label} (Confidence: {confidence_pct}%)")
    else:
        st.success(f"{pred_label} (Confidence: {confidence_pct}%)")

    st.markdown("#### 🔍 Input Summary")
    st.dataframe(pd.DataFrame([input_data]).T.rename(columns={0: "Value"}), height=500)
