# PaperBridge – Multilingual Research Assistant 🧠🌍

**PaperBridge** is an open-source multilingual research assistant that lets users upload academic PDFs in any language, ask questions in their native language, and get accurate, LLM-generated answers — all in real time.

## 🚀 Features

- 📄 **PDF Upload**: Supports research papers in various languages.
- 🔍 **Text Extraction**: Uses PyMuPDF; falls back to OCR for scanned/image-based PDFs.
- 🌐 **Language Detection & Translation**: Translates content using NLLB models.
- 💬 **Q&A Engine**: Retrieves top semantic chunks using FAISS and answers via LLM (OpenRouter/Ollama-compatible).
- 🔁 **Real-Time Reasoning**: Displays step-by-step translation, retrieval, and generation updates in the Streamlit UI.
- 🧠 **Multilingual Support**: Works across a wide range of languages and characters.
- 🖥️ **Frontend + Backend**: Built with FastAPI (backend) and Streamlit (frontend) for a smooth user experience.

## 🌎 Use Case

PaperBridge helps researchers, students, and curious minds break language barriers in academic research. Upload a paper in Japanese, ask a question in Hindi, and get your answer in Hindi — all in seconds.

## 📦 Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **ML/NLP**: NLLB, FAISS, HuggingFace Transformers
- **Text Extraction**: PyMuPDF, Tesseract OCR (fallback)
- **Vector Search**: FAISS
- **Q&A**: LLMs via OpenRouter or Ollama

**_This project is still under development — many more features are coming soon._**  
If you have suggestions or run into issues, please [open an issue](https://github.com/multilingual-research-assisstant/issues) and tag me directly. Let’s build this together!


