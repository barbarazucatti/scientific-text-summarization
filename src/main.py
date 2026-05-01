from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from llm import simplify_text


def process_article(pdf_path):
       
    raw_text = extract_text_from_pdf(pdf_path)
    
    print("🧹 Cleaning text...")
        
    print("=== TEXTO LIMPO ===")
    cleaned_text = clean_text(raw_text)
    print(cleaned_text[:500])
    
    print("📄 Extracting text...")

    print("🧠 Simplifying with LLM...")
    simplified = simplify_text(cleaned_text[:2000])  # limite inicial

    return simplified


if __name__ == "__main__":
    result = process_article("data/CRISPR gene editing technology.pdf")
    print(result)