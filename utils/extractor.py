
import re


def extract_information(text):

    information = {
        "Customer Name": "Not found",
        "Invoice Number": "Not found",
        "Date": "Not found",
        "Address": "Not found",
        "Product": "Not found",
        "Quantity": "Not found",
        "Total Amount": "Not found",
        "Payment Status": "Not found"
    }

    patterns = {
        "Invoice Number": r"Invoice Number\s*:\s*(.+)",
        "Customer Name": r"Customer Name\s*:\s*(.+)",
        "Date": r"Date\s*:\s*(.+)",
        "Address": r"Address\s*:\s*(.+)",
        "Product": r"Product\s*:\s*(.+)",
        "Quantity": r"Quantity\s*:\s*(.+)",
        "Total Amount": r"Total Amount\s*:\s*(.+)",
        "Payment Status": r"Payment Status\s*:\s*(.+)"
    }

    for field, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            information[field] = match.group(1).strip()

    return information
