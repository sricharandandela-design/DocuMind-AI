
from utils.classifier import classify_document


test_documents = {
    "Invoice": """
        Invoice Number: INV-2026-001
        Customer Name: Rahul Sharma
        Product: Laptop
        Quantity: 1
        Total Amount: Rs. 55000
        Payment Status: Paid
    """,

    "Identity Document": """
        Government ID
        Identity Number: 123456789
        Date of Birth: 15 November 2005
        Nationality: Indian
    """,

    "Certificate": """
        CERTIFICATE
        This is to certify that Rahul Sharma
        has successfully completed the course.
        Awarded to Rahul Sharma.
    """,

    "Application Form": """
        APPLICATION FORM
        Applicant Name: Rahul Sharma
        Application Number: APP2026
        Personal Details
        Submit Application
    """,

    "Other Document": """
        Welcome to DocuMind AI.
        This is a general information document.
    """
}


print("\n========== DOCUMENT CLASSIFICATION ==========\n")

for document_name, document_text in test_documents.items():

    result = classify_document(document_text)

    print(f"Expected: {document_name}")
    print(f"Predicted: {result}")
    print("---------------------------------------------")

print("\n=============================================")
