
from utils.ocr import extract_text_from_pdf

pdf_path = input("Enter the full PDF path: ")

print("\n==python test_pdf.py======== PDF EXTRACTION RESULT ==========\n")

result = extract_text_from_pdf(pdf_path)

print(result)

print("\n===========================================")
