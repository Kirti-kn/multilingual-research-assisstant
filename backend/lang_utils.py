from langdetect import detect
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
translator = pipeline("translation", model=model, tokenizer=tokenizer)

lang_code_map = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "fr": "fra_Latn",
    "es": "spa_Latn",
    "de": "deu_Latn",
    "bn": "ben_Beng",
    "ko": "kor_Hang",
}

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"
    
def translate_text(text: str, src_lang: str, tgt_lang: str) -> str:
    try:
        src = lang_code_map.get(src_lang, "eng_Latn")
        tgt = lang_code_map.get(tgt_lang, "eng_Latn")

        if len(text) > 512:
            text = text[:512]

        translated = translator(
            text,
            src_lang=src,
            tgt_lang=tgt,
            max_length=256,
            clean_up_tokenization_spaces=True
        )
        return translated[0]['translation_text']
    except Exception as e:
        return f"[Translation error] {str(e)}"
