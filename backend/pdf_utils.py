# pdf_utils.py
import fitz  # PyMuPDF
from google.cloud import vision

# Set your language hint for OCR
DEFAULT_LANG_HINT = "en"

def extract_text_from_pdf_stream(contents: bytes, lang_hint: str = DEFAULT_LANG_HINT):
    """
    Extracts text from a PDF byte stream using PyMuPDF.
    Falls back to Google Vision OCR if text is empty for any page.
    Returns list of sections with page numbers and text.
    """
    doc = fitz.open(stream=contents, filetype="pdf")
    client = vision.ImageAnnotatorClient()

    sections = []

    for i, page in enumerate(doc):
        text = page.get_text().strip()

        # Fallback to OCR if text is empty
        if not text:
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")
            image = vision.Image(content=image_bytes)

            response = client.document_text_detection(
                image=image,
                image_context={"language_hints": [lang_hint]}
            )

            if response.error.message:
                raise Exception(f"OCR failed on page {i+1}: {response.error.message}")
            text = response.full_text_annotation.text.strip()

        sections.append({"page": i + 1, "text": text})

    doc.close()
    return sections

def extract_full_text_and_chunks(sections, chunker, chunk_size=300, overlap=50):
    """
    Extracts full text and chunked segments from the section list.
    Useful for vector index building.
    """
    full_text = " ".join([sec["text"] for sec in sections])
    all_chunks = []
    for sec in sections:
        chunks = chunker(sec["text"], chunk_size=chunk_size, overlap=overlap)
        all_chunks.extend(chunks)
    return full_text, all_chunks
