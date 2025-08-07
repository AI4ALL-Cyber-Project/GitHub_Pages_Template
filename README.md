# 🛡️ Cyber Attack Detection Web App

This project is a machine learning-powered **web application** that detects cyber attacks based on real-world network traffic. It leverages the **CICIDS dataset** to train a predictive model and deploys the model using **Streamlit** for interactive use.

The app enables users to interact with a trained classifier to determine whether a given network input is normal or an attack.

---

## 📚 Dataset: CICIDS 2017

The [CICIDS 2017 dataset](https://www.unb.ca/cic/datasets/ids-2017.html) was created by the Canadian Institute for Cybersecurity and contains realistic network traffic including both benign and malicious behaviors.

It includes attacks such as:
- DoS
- Brute Force
- Botnet
- PortScan
- DDoS
- Web Attack
- Infiltration

---

## 🚀 Live Streamlit App

🔗 [Click here to use the app](https://cyberdetection.streamlit.app)

Deployed via **Streamlit Community Cloud** using the `Isha` branch, which contains the trained model and deployment script.

---

## 🧠 Machine Learning Model

- **Training Dataset**: CICIDS 2017 (preprocessed)
- **Model File**: `new_model.joblib`
- **Branch Location**: [`Isha` branch](https://github.com/AI4ALL-Cyber-Project/GitHub_Pages_Template/tree/Isha)
- **Script**: `app.py` — loads the model and creates a web interface using Streamlit
- **Features**: Model predicts based on selected input features extracted from the dataset



