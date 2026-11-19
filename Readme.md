# DocuMind AI — Intelligent Document Understanding & Information Extraction

## 1. Project Overview

DocuMind AI is a Python Flask-based web application that automatically reads documents, extracts useful information, classifies document types, and stores processed document records.

The application supports PDF and image documents using Optical Character Recognition (OCR).

## 2. Features

- **Document Upload:** Upload PDF, PNG, JPG, and JPEG files.
- **OCR Processing:** Extract text from uploaded documents using Tesseract OCR.
- **Information Extraction:** Extract invoice details such as customer name, invoice number, date, address, product, quantity, total amount, and payment status.
- **Document Classification:** Identify document categories using keyword-based classification.
- **Dashboard:** Display document statistics and analytics charts.
- **Document History:** View previously uploaded and processed documents.
- **Smart Search:** Search documents using filenames, extracted text, and information.
- **Document Preview:** Preview uploaded PDFs and images.
- **Document Details:** View extracted information and full OCR text.
- **Delete Documents:** Remove document records and associated uploaded files.
- **Download OCR Text:** Download extracted text as a TXT file.
- **Excel Export:** Export extracted information into an Excel spreadsheet.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| HTML | Web page structure |
| CSS | Web page styling |
| JavaScript | Interactive features |
| Tesseract OCR | Text recognition |
| PyMuPDF | PDF processing |
| Pillow | Image processing |
| OpenCV | Image processing |
| Pandas | Data handling |
| OpenPyXL | Excel export |
| Chart.js | Dashboard charts |

## 4. Project Structure

```text
DocuMind-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── document_history.json
│
├── templates/
│   ├── index.html
│   ├── history.html
│   └── document_details.html
│
├── static/
│
├── uploads/
│
├── utils/
│   ├── ocr.py
│   ├── extractor.py
│   ├── stats.py
│   └── classifier.py
│
└── venv/
```

## 5. Installation and Setup

### Step 1: Install Python

Install Python and make sure it is available in your Windows PATH.

### Step 2: Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\venv\Scripts\activate
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Install Tesseract OCR

Install Tesseract OCR for Windows.

Configure its executable path in `config.py`:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## 6. Run the Application

Open the VS Code terminal, activate the virtual environment, and execute:

```powershell
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 7. How It Works

1. The user uploads a PDF or image.
2. The application processes the document using OCR.
3. Extracted text is passed to the information extraction module.
4. The classifier identifies the document category.
5. Document information and OCR text are stored in document history.
6. The dashboard displays document statistics and analytics.
7. Users can view, search, preview, download, delete, and export document information.

## 8. Classification Method

DocuMind AI currently uses keyword-based document classification.

Supported categories include:

- Invoice
- Identity Document
- Certificate
- Application Form
- Other Document

The classifier identifies document categories by checking for relevant keywords in extracted text.

## 9. Future Enhancements

- Machine learning-based document classification.
- Improved information extraction using NLP.
- Support for additional document formats.
- Advanced document analytics.
- Improved OCR accuracy.

## 10. Conclusion

DocuMind AI simplifies document processing by combining OCR, information extraction, document classification, and analytics in one web application.

It helps reduce manual data entry and makes document information easier to access and manage.

---

**Project:** DocuMind AI  
**Type:** Intelligent Document Understanding & Information Extraction  
**Framework:** Python Flask