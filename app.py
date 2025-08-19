import streamlit as st
import requests

st.title("AI Code Generation Agent")

# Input for task description
task = st.text_area("Enter your code generation task:")

if st.button("Generate Code"):
    api_url = "http://127.0.0.1:8000/generate-code"
    response = requests.post(api_url, json={"task_description": task})

    if response.status_code == 200:
        result = response.json()

        st.subheader("Generated Code")
        st.code(result["code"], language="python")

        st.subheader("Generated Tests")
        st.code(result["tests"], language="python")

        st.subheader("Test Output")
        st.text(result["output"])
    else:
        st.error("Failed to get a response from the API")