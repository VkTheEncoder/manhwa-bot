import fitz  # PyMuPDF
import os

def pdf_to_images(pdf_path: str, out_dir: str):
    doc = fitz.open(pdf_path)
    images = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        filename = os.path.join(out_dir, f'{i+1:03}.png')
        pix.save(filename)
        images.append(filename)
    return images
