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


    print(text[:2000])



