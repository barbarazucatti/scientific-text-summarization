from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text

file_path = "data/CRISPR gene editing technology.pdf"

raw_text = extract_text_from_pdf(file_path)
cleaned_text = clean_text(raw_text)

print("ANTES:\n", raw_text[:300])
print("\n\nDEPOIS:\n", cleaned_text[:300])