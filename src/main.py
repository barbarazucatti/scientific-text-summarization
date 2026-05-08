from llm import simplify_text
from llm_processor import build_article_digest
from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text, extract_scientific_sections


def process_article(pdf_path):
    print("Extracting text...")
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text.strip():
        return "Nao foi possivel extrair texto desse PDF. Verifique se ele nao e apenas imagem/scaneado."

    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)

    print("Extracting scientific sections...")
    sections = extract_scientific_sections(cleaned_text)

    print("Preparing article digest...")
    article_digest = build_article_digest(sections, full_text=cleaned_text)

    if not article_digest.strip():
        return "Nao foi possivel preparar o texto desse PDF para explicacao."

    print(f"Digest size: {len(article_digest)} characters")
    print("Generating final explanation...")
    final_result = simplify_text(article_digest)

    print("\n=== RESULTADO FINAL ===\n")
    print(final_result)

    return final_result


if __name__ == "__main__":
    print("Script started")
    result = process_article("../data/CRISPR gene editing technology.pdf")
    print("\n=== RESULTADO FINAL ===\n")
    print(result)
