import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tickers_cred.json"

from google.cloud import vision
import io
import cv2

def perform_ocr(image):
    client = vision.ImageAnnotatorClient()

    # Perform OCR on the image
    image_data = cv2.imencode('.jpg', image)[1].tostring()  # Convert image to bytes
    ocr_image = vision.Image(content=image_data)

    # Specify the language hint for Urdu
    image_context = vision.ImageContext(language_hints=["ur"])

    response = client.text_detection(image=ocr_image, image_context=image_context)
    texts = response.text_annotations

    return texts[0].description
