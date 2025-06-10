import os
from google.cloud import vision
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("google_credentials.json")
client = vision.ImageAnnotatorClient(credentials=credentials)

def ocr_image_bytes(image_bytes: bytes) -> str:
    image = vision.Image(content=image_bytes)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    return response.full_text_annotation.text