from fastapi import APIRouter, UploadFile, File, Form
from backend.summarizer import summarize_section
from backend.lang_utils import detect_language, translate_text
from backend.qa_utils import build_vector_store, query_top_k, chunk_text
from backend.llm_utils import generate_answer
from backend.pdf_utils import extract_text_from_pdf_stream
import fitz

router = APIRouter()
pdf_language = "en"

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error":"Only PDF files are supported."}
    
    contents = await file.read()
    sections = extract_text_from_pdf_stream(contents)

    return {"sections": sections}

@router.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}
    
    contents = await file.read()
    pdf_doc = fitz.open(stream=contents, filetype="pdf")

    summaries = []
    for i, page in enumerate(pdf_doc):
        text = page.get_text().strip()
        summary = summarize_section(text)
        summaries.append({
            "page": i+1,
            "summary": summary
        })

    return {"summaries": summaries}

@router.post("/translate")
async def translate_text_api(text: str):
    detected = detect_language(text)
    translated = translate_text(text, src_lang=detected, tgt_lang="en")
    return {
        "detected_language": detected,
        "translated_text": translated
    }

@router.post("/build-index/")
async def build_index(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_doc = fitz.open(stream=contents, filetype="pdf")

    full_text = ""
    all_chunks = []
    for page in pdf_doc:
        text = page.get_text().strip()
        full_text += text + " "
        chunks = chunk_text(text, chunk_size=300, overlap=50)
        all_chunks.extend(chunks)

    build_vector_store(all_chunks)

    global pdf_language
    pdf_language = detect_language(full_text[:1000])

    return {"status": f"Indexed {len(all_chunks)} chunks", "pdf_language": pdf_language}


@router.get("/query/")
async def query(question: str):
    results = query_top_k(question)
    return {"matches":results}

@router.post("/ask/")
async def ask(question: str = Form(...)):
    updates = []

    detected_lang = detect_language(question)
    updates.append(f"User language detected: {detected_lang}")

    translated_question = translate_text(question, src_lang=detected_lang, tgt_lang=pdf_language)
    updates.append("Question translated to PDF language")

    top_chunks = query_top_k(translated_question)
    updates.append("Top chunks retrieved")

    context = "\n".join(top_chunks)
    updates.append("Chunks joined for context")

    answer_in_pdf_lang = generate_answer(context, translated_question)
    updates.append("Answer generated in PDF language")

    final_ans = translate_text(answer_in_pdf_lang, src_lang=pdf_language, tgt_lang=detected_lang)
    updates.append("Final answer translated")

    return {
        "updates": updates,
        "detected_language": detected_lang,
        "pdf_language": pdf_language,
        "translated_question": translated_question,
        "answer_in_pdf_lang": answer_in_pdf_lang,
        "final_answer": final_ans
    }
