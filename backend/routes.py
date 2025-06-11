from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from backend.summarizer import summarize_section
from backend.lang_utils import detect_language, translate_text
from backend.qa_utils import build_vector_store, query_top_k, chunk_text
from backend.llm_utils import generate_answer
from backend.pdf_utils import extract_text_from_pdf_stream
import fitz
import asyncio

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

@router.post("/ask-stream/")
async def ask_stream(question: str = Form(...)):
    async def event_stream():
        yield "User language detected\n"
        user_lang = detect_language(question)
        await asyncio.sleep(0.5)

        yield "Question translated to PDF language\n"
        translated_question = translate_text(question, src_lang=user_lang, tgt_lang=pdf_language)
        await asyncio.sleep(0.5)

        yield "Top chunks retrieved\n"
        top_chunks = query_top_k(translated_question)
        await asyncio.sleep(0.5)

        yield "Chunks joined for context\n"
        context = "\n".join(top_chunks)
        await asyncio.sleep(0.5)

        yield "Generating answer...\n"
        answer_in_pdf_lang = generate_answer(context, translated_question)
        await asyncio.sleep(0.5)

        yield "Answer generated in PDF language\n"
        await asyncio.sleep(0.3)

        yield "Translating answer to user's language\n"
        final_ans = translate_text(answer_in_pdf_lang, src_lang=pdf_language, tgt_lang=user_lang)
        await asyncio.sleep(0.5)

        yield f"DONE::{final_ans}\n"

    return StreamingResponse(event_stream(), media_type="text/plain")
