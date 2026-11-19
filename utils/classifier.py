
import re


def classify_document(text):

    text = text.lower()

    document_types = {
        "Invoice": [
            "invoice",
            "invoice number",
            "total amount",
            "payment status",
            "quantity"
        ],

        "Identity Document": [
            "date of birth",
            "identity number",
            "nationality",
            "government id",
            "identification"
        ],

        "Certificate": [
            "certificate",
            "this is to certify",
            "has successfully completed",
            "certified that",
            "awarded to"
        ],

        "Application Form": [
            "application form",
            "applicant name",
            "application number",
            "submit application",
            "personal details"
        ]
    }

    scores = {}

    for document_type, keywords in document_types.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[document_type] = score

    best_type = max(scores, key=scores.get)

    if scores[best_type] == 0:
        return "Other Document"

    return best_type
