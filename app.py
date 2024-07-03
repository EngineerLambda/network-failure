import streamlit as st
import joblib
import time


@st.cache_resource
def load_model_and_scaler():
    model = joblib.load("logreg.pkl")
    scaler = joblib.load("scaler.pkl")
    
    return model, scaler


model, scaler = load_model_and_scaler()

st.title("Web App For Predicting Failure in Networking Devices - A Demo")

device_map = {
    "Router/Gateway" : 0,
    "Firewall" : 1,
    "Switch" : 2,
    "AP" : 3,
    "Server" : 4,
    "Laptop" : 5
}

device_type = st.selectbox("Select device type", options=device_map.keys())
temp = st.number_input("What is the device's temperature in ℃?")
cpu_usage = st.number_input("What is the device's CPU usage?")
mem_usage = st.number_input("What is the device's memory usage?")
error_rate = st.number_input("What is the device's error rate?")
uptime = st.number_input("What is the device's uptime in seconds (e.g 16.2)")

array = [device_map.get(device_type), temp, cpu_usage, mem_usage, error_rate, uptime]


if st.button("Predict Failure"):
    if all(array[1:]):
        with st.spinner("Predicting ..."):
            time.sleep(2)
            full_array = [array]
            scaled_array = scaler.transform(full_array)
            
            prediction = model.predict(scaled_array)
            if prediction == 0:
                st.success("Failure not predicted for this device")
            else:
                st.error("Device is predicted to fail")

    else:
        st.warning("kindly supply all the input values")
    