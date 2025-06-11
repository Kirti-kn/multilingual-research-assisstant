import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="PaperBridge", layout="wide")
st.title("📚 PaperBridge — Your Multilingual Research Assistant")

st.header("Step 1: Upload PDF and Build Index")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
build_status = st.empty()

if uploaded_file:
    with st.spinner("Uploading and indexing PDF..."):
        res = requests.post(
            f"{BACKEND_URL}/build-index/",
            files={"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
        )
        if res.ok:
            result = res.json()
            build_status.success(f"✅ {result['status']}, Language: {result['pdf_language']}")
        else:
            build_status.error("❌ Failed to build index.")

st.header("Step 2: Ask a Question")
question = st.text_input("Enter your question")

if st.button("Ask") and question:
    with st.spinner("Processing your question..."):
        response = requests.post(
            f"{BACKEND_URL}/ask-stream/",
            data={"question": question},
            stream=True
        )
        status_box = st.empty()
        answer_box = st.empty()

        updates = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                if line.startswith("DONE::"):
                    answer_box.success(line.replace("DONE::", ""))
                    break
                else:
                    updates += f"- {line}\n"
                    status_box.markdown(updates)
