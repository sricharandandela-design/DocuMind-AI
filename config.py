
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
