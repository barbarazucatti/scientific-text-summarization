import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # ----------------------------
    # 1. Corrigir ligaduras
    # ----------------------------
    text = (text
        .replace("ﬁ", "fi")
        .replace("ﬂ", "fl")
        .replace("ﬀ", "ff")
    )

    # ----------------------------
    # 2. Remover URLs
    # ----------------------------
    text = re.sub(r"http\S+|www\.\S+", "", text)

    # ----------------------------
    # 3. Remover cabeçalhos comuns (mais seguro)
    # ----------------------------
    text = re.sub(r"\b(REVIEW ARTICLE|OPEN|IMMUNOTHERAPY)\b", "", text, flags=re.IGNORECASE)

    # ----------------------------
    # 4. Remover copyright
    # ----------------------------
    text = re.sub(r"©.*?\d{4}", "", text)

    # ----------------------------
    # 5. Remover autores (padrão mais específico)
    # ----------------------------
    text = re.sub(r"(?:[A-Z][a-z]+\s[A-Z][a-z]+(?:\d+,?\s*)?)+(?=,|\n)", "", text)

    # ----------------------------
    # 6. Remover números soltos estranhos
    # ----------------------------
    text = re.sub(r"\b\d+(?:,\s*\d+)+\b", "", text)

    # ----------------------------
    # 7. Corrigir palavras grudadas (MELHORADO)
    # ----------------------------
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])(\()", r"\1 \2", text)

    # ----------------------------
    # 8. Corrigir espaços
    # ----------------------------
    text = re.sub(r"\s+", " ", text)

    # ----------------------------
    # 9. Limpar caracteres estranhos
    # ----------------------------
    text = re.sub(r"[^\w\s.,;:()\-/]", "", text)
    
    # ----------------------------
    # 10. Corrigir letras + números colados
    # ----------------------------
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)

    # ----------------------------
    # 11. Remover padrões de afiliação (números soltos com vírgula)
    # ----------------------------
    text = re.sub(r"(,\s*\d+\s*)+", "", text)
    
    # ----------------------------
    # 12. Remover vírgulas soltas e lixo residual
    # ----------------------------
    text = re.sub(r"(,\s*){2,}", ", ", text)   # várias vírgulas → 1
    text = re.sub(r"\s+,", ",", text)          # espaço antes de vírgula
    text = re.sub(r",\s*,", ", ", text)        # vírgulas duplicadas

    # ----------------------------
    # 13. Remover nomes isolados com números (resto de autores)
    # ----------------------------
    text = re.sub(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\s\d+(?:\sand\s\d+)?\b", "", text)

    return text.strip()

def extract_scientific_sections(text):
    text = text.replace("\n", " ")

    patterns = {
        "abstract": r"(abstract)(.*?)(introduction|1\.)",
        "introduction": r"(introduction)(.*?)(methods|materials and methods|2\.)",
        "methods": r"(methods|materials and methods)(.*?)(results|3\.)",
        "results": r"(results)(.*?)(discussion|4\.)",
        "discussion": r"(discussion)(.*?)(references|conclusion|5\.)",
        "conclusion": r"(conclusion)(.*?)(references|$)"
    }

    sections = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(2).strip()
        else:
            sections[key] = ""

    return sections