import pytesseract
from PIL import Image

def ocr_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang='eng')
