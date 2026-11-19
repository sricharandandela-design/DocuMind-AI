
import pytesseract
import fitz
from PIL import Image
from config import TESSERACT_PATH

# Connect Python with Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)

        extracted_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        return extracted_text.strip()

    except Exception as error:
        return f"OCR Error: {error}"


def extract_text_from_pdf(pdf_path):
    try:
        extracted_text = ""

        pdf_document = fitz.open(pdf_path)

        for page_number, page in enumerate(pdf_document):
            page_text = page.get_text()

            if page_text.strip():
                extracted_text += page_text + "\n"
            else:
                # OCR scanned PDF pages
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                page_ocr = pytesseract.image_to_string(
                    image,
                    lang="eng"
                )

                extracted_text += page_ocr + "\n"

        pdf_document.close()

        return extracted_text.strip()

    except Exception as error:
        return f"PDF Error: {error}"
