import os
import requests

import streamlit as st

st.title("AI Code Generation Agent")

# Input for task description
task = st.text_area("Enter your code generation task:")

if st.button("Generate Code"):

    # Get the API URL from the environment variable, with a default for local development
    api_base_url = os.getenv("API_URL", "http://127.0.0.1:8000")
    api_url = f"{api_base_url}/generate-code"
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