import os
from google.cloud import vision
# from google.cloud.vision import types

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "scripts/tickers.json"

def detect_text_uri(uri):
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image, image_context={"language_hints": ["ur"]})
    texts = response.text_annotations

    for text in texts:
        print('\n"{}"'.format(text.description))

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check:''https://cloud.google.com/apis/design/errors'.format(response.error.message))

# Example usage
image_uri = "assets/tickers/ary/ary_frame_2023-08-14_16-21-30.jpg"
detect_text_uri(image_uri)

