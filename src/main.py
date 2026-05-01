from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from text_cleaner import extract_scientific_sections

from llm_processor import chunk_by_section, simplify_chunks
from llm import simplify_text, merge_summaries

from openai import OpenAI

client = OpenAI()


def process_article(pdf_path):

    print("📄 Extracting text...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("🧹 Cleaning text...")
    cleaned_text = clean_text(raw_text)

    print("🔎 Extracting scientific sections...")
    sections = extract_scientific_sections(cleaned_text)

    print("✂️ Chunking by section...")
    chunks = chunk_by_section(sections)

    print(f"Total structured chunks: {len(chunks)}")

    print("🧠 Simplifying chunks...")
    simplified_chunks = simplify_chunks(chunks, simplify_text)

    print("🧠 Merging...")
    final_result = merge_summaries(simplified_chunks, client)

    print("\n=== RESULTADO FINAL ===\n")
    print(final_result)

    return final_result


if __name__ == "__main__":
    print("🚀 Script iniciou")
    result = process_article("../data/CRISPR gene editing technology.pdf")
    print("\n=== RESULTADO FINAL ===\n")
    print(result)
