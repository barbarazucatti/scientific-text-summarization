from openai import OpenAI

client = OpenAI()

def simplify_text(text):
    
    print(">>> TEXTO REAL RECEBIDO:")
    print(repr(text))
    
    prompt = f"""
You are an assistant that rewrites scientific content for non-experts while preserving depth and accuracy.

Your goal is to make the text easier to understand WITHOUT losing important scientific details.

Guidelines:
- Preserve specific methods, techniques, and named concepts (e.g., CRISPR, CAR-T cells)
- DO NOT remove important details or mechanisms
- Explain ideas clearly, but keep the explanation informative and not superficial
- You MAY briefly clarify technical terms in the text, but do not overload it
- Provide a more complete explanation (not just 1–2 sentences)
- Avoid vague phrases like "improves treatment" — explain how and why
- Keep a balance between clarity and technical accuracy

Key Concepts section:
- List and explain the main scientific terms mentioned in the text
- Include specific methods (e.g., CRISPR, CAR-T)
- Do not repeat generic concepts unless necessary

Text:
{text}

Return in this format:

### Simplified Explanation:
(Write a clear, structured explanation with enough detail to truly understand the idea)

### Key Concepts Explained:
- Term: explanation
- Term: explanation
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text


    print(text[:2000])



