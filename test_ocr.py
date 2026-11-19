
from utils.ocr import extract_text_from_image

image_path = input("Enter the full image path: ")

print("\n========== OCR RESULT ==========\n")

result = extract_text_from_image(image_path)

print(result)

print("\n================================")
