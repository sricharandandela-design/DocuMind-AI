
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HISTORY_FILE = os.path.join(BASE_DIR, "document_history.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_document(
    filename,
    extracted_information,
    document_type="Other Document",
    extracted_text=""
):
    history = load_history()

    history.append({
        "filename": filename,
        "status": "Processed",
        "document_type": document_type,
        "extracted_information": extracted_information,
        "extracted_text": extracted_text
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def get_dashboard_stats():
    history = load_history()

    total_documents = len(history)

    processed_documents = sum(
        1 for document in history
        if document.get("status") == "Processed"
    )

    extracted_fields = sum(
        1
        for document in history
        for value in document.get("extracted_information", {}).values()
        if value != "Not found" and value
    )

    return {
        "total_documents": total_documents,
        "processed_documents": processed_documents,
        "extracted_fields": extracted_fields
    }


def get_document_type_stats():
    history = load_history()

    categories = {
        "Invoice": 0,
        "Identity Document": 0,
        "Certificate": 0,
        "Application Form": 0,
        "Other Document": 0,
        "Not classified": 0
    }

    for document in history:
        document_type = document.get(
            "document_type",
            "Not classified"
        )

        if document_type in categories:
            categories[document_type] += 1
        else:
            categories["Other Document"] += 1

    return categories


def delete_document(document_index):
    history = load_history()

    if document_index < 0 or document_index >= len(history):
        return False

    document = history.pop(document_index)
    filename = document.get("filename")

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    filename_still_used = any(
        item.get("filename") == filename
        for item in history
    )

    if filename and not filename_still_used:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

    return True
