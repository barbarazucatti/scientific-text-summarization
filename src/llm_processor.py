def chunk_by_section(sections, max_chars=1500):
    chunks = []

    section_weights = {
        "abstract": 1.5,
        "results": 2.0,
        "discussion": 1.5,
        "introduction": 1.0,
        "methods": 1.0,
        "conclusion": 1.2
    }

    for section_name, text in sections.items():
        if not text:
            continue

        sentences = text.split(". ")

        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chars:
                current_chunk += sentence + ". "
            else:
                chunks.append({
                    "section": section_name,
                    "text": current_chunk.strip()
                })
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append({
                "section": section_name,
                "text": current_chunk.strip()
            })

    return chunks

def simplify_chunks(chunks, simplify_text_fn):
    results = []

    for i, chunk in enumerate(chunks):
        print(f"Processing {chunk['section']} chunk {i+1}/{len(chunks)}")

        prompt_input = f"""
        SECTION: {chunk['section']}

        TEXT:
        {chunk['text']}
        """

        simplified = simplify_text_fn(prompt_input)
        results.append(simplified)

    return results

def merge_summaries(summaries, client):
    combined_text = "\n\n".join(summaries)

    prompt = f"""
You are merging multiple partial summaries of a scientific article.

STRICT RULES:
- Do NOT introduce new information
- Do NOT infer or generalize beyond what is explicitly stated
- Do NOT create examples, studies, or results unless they appear in the summaries
- If information is inconsistent or unclear, keep it generic rather than guessing
- Prefer loss of detail over introducing incorrect information
- Do NOT combine ideas into a narrative unless they are clearly connected

Your goal is to:
- Consolidate overlapping information
- Remove redundancy
- Preserve only what is explicitly supported

Summaries:
{combined_text}

Return:

### Simplified Explanation:
...

### Key Concepts Explained:
- Term: explanation
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text