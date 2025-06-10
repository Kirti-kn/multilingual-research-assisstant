import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Change if hosted elsewhere

st.set_page_config(page_title="Multilingual Research Assistant", layout="wide")
st.title("📚 Multilingual Research Assistant")

# Upload PDF and build index
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

# Ask questions
st.header("Step 2: Ask a Question")
question = st.text_input("Enter your question")

if st.button("Ask") and question:
    with st.spinner("Processing your question..."):
        res = requests.post(f"{BACKEND_URL}/ask/", data={"question": question})
        if res.ok:
            data = res.json()
            st.subheader("📝 Answer")
            st.write(data['final_answer'])

            st.subheader("🛠️ Translation and Processing Steps")
            for step in data["updates"]:
                st.markdown(f"- {step}")
        else:
            st.error("❌ Failed to generate answer.")
