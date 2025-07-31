import streamlit as st
import joblib
import numpy as np
import pandas as pd
import json
import time

# Load model and features
model = joblib.load("new_model.joblib")
feature_names = model.feature_names_in_

with open("feature_ranges.json", "r") as f:
    feature_ranges = json.load(f)

# Dark mode CSS
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

# Page title
st.set_page_config(page_title="🛡️ Real-Time Intrusion Detection", layout="wide")
st.sidebar.title("Settings")

# Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "benign_streak" not in st.session_state:
    st.session_state.benign_streak = 0

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("🌗 Toggle Dark Mode", on_click=toggle_dark_mode)

if st.session_state.dark_mode:
    st.markdown(dark_mode_css,unsafe_allow_html=True)
else:
    st.markdown(light_mode_css,unsafe_allow_html=True)

# different tabs 
tab1, tab2 = st.tabs(["✍️ Manual Prediction", "📡 Live Stream Simulation"])


# Tab 1: Manual Prediction
with tab1:
    st.title("🛡️ Real-Time Intrusion Detection System")
    st.caption("Manually enter or simulate features to detect if traffic is benign or an attack.")
    st.markdown("### Input Options")

    # Initialize
    for feature in feature_names:
        if feature not in st.session_state:
            low, high = feature_ranges.get(feature,(0, 1))
            st.session_state[feature]=round((low + high)/2,5)

    # Simulate input
    def generate_random_input():
        for feature in feature_names:
            low, high = feature_ranges.get(feature,(0, 1))
            st.session_state[feature]=round(np.random.uniform(low,high),5)

    col_sim, _ = st.columns([1, 4])
    with col_sim:
        if st.button("🎲 Simulate Random Data"):
            generate_random_input()
            st.success("Random values generated.")

    # Input Form
    with st.form("prediction_form"):
        st.markdown("### ✍️ Feature Input")
        input_data = {}

        left_col, right_col = st.columns(2)
        for i, feature in enumerate(feature_names):
            low, high = feature_ranges.get(feature, (0, 1))
            default_val = st.session_state[feature]
            step = (high-low)/1000 if (high-low)>0 else 0.01

            if i % 2 == 0:
                vals=left_col.slider(feature,float(low),float(high),float(default_val),step=step,format="%.5f")
            else:
                vals=right_col.slider(feature,float(low),float(high),float(default_val),step=step,format="%.5f")

            input_data[feature]=vals
            st.session_state[feature]=vals

        submitted = st.form_submit_button("🚀 Predict")

    # Prediction using the model
    if submitted:
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        prediction_pro = model.predict_proba(input_df)[0]
        confi = max(prediction_pro)
        confidence_pct = round(confi*100,2)

        if isinstance(prediction, (int, np.integer)):
            label = "🚨 **Attack**" if prediction == 1 else "✅ **Benign**"
        else:
            label = "🚨 **Attack**" if str(prediction).lower() == "attack" else "✅ **Benign**"

        st.markdown("---")
        st.markdown("## 🧠 Prediction Result")
        if "attack" in label.lower():
            st.error(f"{label} (Confidence: {confidence_pct}%)")
        else:
            st.success(f"{label} (Confidence: {confidence_pct}%)")

        st.markdown("#### 🔍 Input Summary")
        st.dataframe(pd.DataFrame([input_data]).T.rename(columns={0: "Value"}), height=500)

# Tab 2: Live Stream Simulation

with tab2:
    st.title("📡 Live Stream Intrusion Simulation")
    st.caption("Streaming randomized benign and attack traffic. This aims to stimulate real-time network traffic")

    num_packets = st.slider("Number of packets to simulate", 5, 100, 20)
    delay = st.slider("Delay between packets (sec)", 0.1, 2.0, 0.5)

    if st.button("Start Live Simulation"):
        results = []
        seen_benign = False
        seen_attack = False
        placeholder = st.empty()

        for i in range(num_packets):
            # Decide label randomly, ensuring both appear at least once
            if i >= num_packets - 2:
                if not seen_attack:
                    is_attack = True
                elif not seen_benign:
                    is_attack = False
                else:
                    is_attack = np.random.rand()<0.5
            else:
                is_attack = np.random.rand()<0.5

            if is_attack:
                seen_attack = True
            else:
                seen_benign = True

            row = {}
            for feat in feature_names:
                low, high = feature_ranges.get(feat, (0, 1))
                row[feat] = round(np.random.uniform(low, high), 5)

            input_df = pd.DataFrame([row])
            pred_label = "🚨 Attack" if is_attack else "✅ Benign"

            # Adding metadata
            row["Packet"] = i + 1
            row["Prediction"] = pred_label
            row["Time"] = time.strftime("%H:%M:%S")

            results.append(row)

            
            placeholder.dataframe(pd.DataFrame(results[-10:]), use_container_width=True)

            time.sleep(delay)

        # full display
        df = pd.DataFrame(results)
        st.markdown("### 📊 Full Stream Log")
        st.dataframe(df, use_container_width=True, height=500)

        # Benign / Attack filters
        with st.expander("🟢 Benign Packets"):
            st.dataframe(df[df["Prediction"]== "✅ Benign"], use_container_width=True)

        with st.expander("🔴 Attack Packets"):
            st.dataframe(df[df["Prediction"]== "🚨 Attack"], use_container_width=True)

        # Download csv file
        csv = df.to_csv(index=False)
        st.download_button("📥 Download as CSV", data=csv, file_name="live_stream_log.csv", mime="text/csv")
