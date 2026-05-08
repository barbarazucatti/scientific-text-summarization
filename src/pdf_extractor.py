import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    pages = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages.append(page.get_text("text"))

    return "\n\n".join(pages)
