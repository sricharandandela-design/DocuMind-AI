
import os
from io import BytesIO

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    send_file,
    send_from_directory
)

from werkzeug.utils import secure_filename
from openpyxl import Workbook

from utils.ocr import extract_text_from_image, extract_text_from_pdf
from utils.extractor import extract_information
from utils.classifier import classify_document

from utils.stats import (
    save_document,
    get_dashboard_stats,
    get_document_type_stats,
    load_history,
    delete_document
)


app = Flask(__name__)

app.secret_key = "documind_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():

    stats = get_dashboard_stats()
    category_stats = get_document_type_stats()

    return render_template(
        "index.html",
        stats=stats,
        category_stats=category_stats
    )


@app.route("/history")
def history():

    documents = load_history()

    search_query = request.args.get("search", "").strip()
    selected_type = request.args.get("document_type", "").strip()
    selected_status = request.args.get("status", "").strip()

    filtered_documents = []

    for original_index, document in enumerate(documents):

        filename = document.get("filename", "")
        document_type = document.get("document_type", "Not classified")
        status = document.get("status", "")

        extracted_text = document.get("extracted_text", "")

        extracted_information = document.get(
            "extracted_information", {}
        )

        searchable_content = " ".join([
            filename,
            extracted_text,
            " ".join(str(value) for value in extracted_information.values())
        ])

        if (
            search_query
            and search_query.lower() not in searchable_content.lower()
        ):
            continue

        if selected_type and document_type != selected_type:
            continue

        if selected_status and status != selected_status:
            continue

        filtered_documents.append({
            "document": document,
            "original_index": original_index
        })

    return render_template(
        "history.html",
        documents=filtered_documents,
        search_query=search_query,
        selected_type=selected_type,
        selected_status=selected_status
    )


@app.route("/document/<int:document_index>")
def document_details(document_index):

    documents = load_history()

    if document_index < 0 or document_index >= len(documents):
        abort(404)

    document = documents[document_index]

    return render_template(
        "document_details.html",
        document=document,
        document_index=document_index
    )


@app.route("/download-text/<int:document_index>")
def download_extracted_text(document_index):

    documents = load_history()

    if document_index < 0 or document_index >= len(documents):
        abort(404)

    document = documents[document_index]

    extracted_text = document.get("extracted_text", "")

    if not extracted_text:
        flash("No extracted OCR text is available to download.")
        return redirect(
            url_for("document_details", document_index=document_index)
        )

    output = BytesIO(extracted_text.encode("utf-8"))
    output.seek(0)

    original_filename = document.get("filename", "document")
    base_filename = os.path.splitext(original_filename)[0]
    download_filename = f"{base_filename}_OCR_Text.txt"

    return send_file(
        output,
        as_attachment=True,
        download_name=download_filename,
        mimetype="text/plain"
    )


@app.route("/preview/<path:filename>")
def preview_document(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False
    )


@app.route("/delete/<int:document_index>", methods=["POST"])
def remove_document(document_index):

    success = delete_document(document_index)

    if success:
        flash("Document deleted successfully!")
    else:
        flash("Document not found!")

    return redirect(url_for("history"))


@app.route("/export")
def export_excel():

    documents = load_history()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "DocuMind Results"

    fields = [
        "Customer Name",
        "Invoice Number",
        "Date",
        "Address",
        "Product",
        "Quantity",
        "Total Amount",
        "Payment Status"
    ]

    headers = ["Document Name", "Document Type", "Status"] + fields
    worksheet.append(headers)

    for document in documents:

        information = document.get("extracted_information", {})

        row = [
            document.get("filename", ""),
            document.get("document_type", "Not classified"),
            document.get("status", "")
        ]

        for field in fields:
            row.append(information.get(field, "Not found"))

        worksheet.append(row)

    for column in worksheet.columns:

        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))

        worksheet.column_dimensions[column_letter].width = max_length + 3

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="DocuMind_Extracted_Data.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/upload", methods=["POST"])
def upload_file():

    if "document" not in request.files:
        flash("No document selected!")
        return redirect(url_for("home"))

    file = request.files["document"]

    if file.filename == "":
        flash("Please select a document!")
        return redirect(url_for("home"))

    if not allowed_file(file.filename):
        flash("Invalid file type. Upload PDF, JPG or PNG.")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    extension = filename.rsplit(".", 1)[1].lower()

    if extension == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
    else:
        extracted_text = extract_text_from_image(file_path)

    if extracted_text.startswith(("OCR Error:", "PDF Error:")):
        flash(extracted_text)
        return redirect(url_for("home"))

    extracted_information = extract_information(extracted_text)

    document_type = classify_document(extracted_text)

    save_document(
        filename,
        extracted_information,
        document_type,
        extracted_text
    )

    stats = get_dashboard_stats()
    category_stats = get_document_type_stats()

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        extracted_information=extracted_information,
        uploaded_filename=filename,
        document_type=document_type,
        stats=stats,
        category_stats=category_stats
    )


if __name__ == "__main__":
    app.run(debug=True)
