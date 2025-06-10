from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_section(text: str) -> str:
    if len(text.strip()) < 20:
        return "Too short to summarize."
    
    max_input_len = 1024
    input_text = text.strip()[:max_input_len]

    summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']