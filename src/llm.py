from openai import OpenAI

client = OpenAI()

def simplify_text(text):
    
    print(">>> TEXTO REAL RECEBIDO:")
    print(repr(text))
    
    prompt = f"""
You are an assistant that rewrites scientific content for non-experts while preserving important details.

Your goal is to make the text easier to understand WITHOUT reducing its level of detail.

Guidelines:
- DO NOT remove or generalize specific techniques, methods, or named concepts (e.g., CRISPR, CAR-T cells)
- DO NOT shorten the content significantly
- Preserve cause-effect relationships and mechanisms described in the text
- If the input is detailed, the output MUST also be detailed
- Do NOT explain technical terms inside the main text
- List and explain all important technical terms in the "Key Concepts Explained" section
- Ensure that every important term from the text is included in the Key Concepts section
- You may include additional terms ONLY if necessary for understanding
- Avoid vague explanations — be specific about how things work
- Each concept MUST be on a new line
- Do NOT merge bullet points
- Do not introduce any information that is not present in the text

STRICT RULES:
- Do NOT add any information that is not explicitly present in the text
- Do NOT infer results, experiments, or clinical outcomes unless clearly stated
- If information is unclear or incomplete, say so instead of guessing
- If specific numbers (e.g., number of patients, results) are not present, do NOT create them
- Only summarize what is directly supported by the text



Text:
{text}

Return in this format:

### Simplified Explanation:
...

### Key Concepts Explained:
- Term: explanation
- Term: explanation
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text


def merge_summaries(summaries, client):

    prompt = f"""
You are merging scientific summaries.

Rules:
- Remove repetition
- Keep structure logical
- Preserve scientific meaning
- Keep it readable for non-experts

Summaries:
{chr(10).join(summaries)}

Return a final unified explanation with:
1. Simple explanation
2. Key concepts
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



