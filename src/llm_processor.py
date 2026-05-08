def _trim_text(text, max_chars):
    text = text.strip()
    if len(text) <= max_chars:
        return text

    head_size = int(max_chars * 0.75)
    tail_size = max_chars - head_size

    return f"{text[:head_size]}\n\n[... trecho intermediario omitido para reduzir tempo ...]\n\n{text[-tail_size:]}"


def build_article_digest(sections, full_text="", max_chars=45000):
    section_budgets = {
        "abstract": 9000,
        "discussion": 12000,
        "conclusion": 7000,
        "results": 10000,
        "introduction": 5000,
        "methods": 2000,
    }

    selected_parts = []
    used_chars = 0

    for section_name, budget in section_budgets.items():
        text = sections.get(section_name, "").strip()
        if not text:
            continue

        remaining = max_chars - used_chars
        if remaining <= 0:
            break

        section_text = _trim_text(text, min(budget, remaining))
        selected_parts.append(f"SECTION: {section_name}\n\n{section_text}")
        used_chars += len(section_text)

    if selected_parts:
        return "\n\n---\n\n".join(selected_parts)

    return _trim_text(full_text, max_chars)


def _split_long_paragraph(paragraph, max_chars):
    sentences = paragraph.split(". ")
    pieces = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if not sentence.endswith("."):
            sentence = f"{sentence}."

        if len(current) + len(sentence) + 1 <= max_chars:
            current = f"{current} {sentence}".strip()
            continue

        if current:
            pieces.append(current)
        current = sentence

    if current:
        pieces.append(current)

    return pieces


def chunk_text(text, max_chars=6000):
    chunks = []
    current = ""

    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        paragraphs = [paragraph]
        if len(paragraph) > max_chars:
            paragraphs = _split_long_paragraph(paragraph, max_chars)

        for piece in paragraphs:
            if len(current) + len(piece) + 2 <= max_chars:
                current = f"{current}\n\n{piece}".strip()
                continue

            if current:
                chunks.append(current)
            current = piece

    if current:
        chunks.append(current)

    return chunks


def chunk_by_section(sections, full_text="", max_chars=6000):
    chunks = []

    priority = [
        "abstract",
        "introduction",
        "methods",
        "results",
        "discussion",
        "conclusion",
    ]

    for section_name in priority:
        text = sections.get(section_name, "").strip()
        if not text:
            continue

        for chunk in chunk_text(text, max_chars=max_chars):
            chunks.append({
                "section": section_name,
                "text": chunk,
            })

    if not chunks and full_text:
        for chunk in chunk_text(full_text, max_chars=max_chars):
            chunks.append({
                "section": "full_text",
                "text": chunk,
            })

    return chunks


def simplify_chunks(chunks, simplify_text_fn):
    results = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Processing {chunk['section']} chunk {index}/{len(chunks)}")

        prompt_input = f"""
SECTION: {chunk['section']}

TEXT:
{chunk['text']}
"""

        simplified = simplify_text_fn(prompt_input)
        results.append(simplified)

    return results
