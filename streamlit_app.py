import streamlit as st
import requests

st.title("Streamlit and Flask Integration")

response = requests.get("http://localhost:5000/")  # Adjust URL for production
if response.status_code == 200:
    st.write(response.json())
else:
    st.write("Error fetching data from Flask API")