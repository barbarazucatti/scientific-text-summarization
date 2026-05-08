import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\ufb00": "ff",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_scientific_sections(text):
    normalized = re.sub(r"\r\n?", "\n", text)

    heading_patterns = {
        "abstract": r"abstract|summary|resumo",
        "introduction": r"introduction|introducao",
        "methods": r"methods|materials and methods|methodology|metodos|materiais e metodos",
        "results": r"results|resultados",
        "discussion": r"discussion|discussao",
        "conclusion": r"conclusion|conclusions|conclusao|consideracoes finais",
        "references": r"references|referencias|bibliography",
    }

    matches = []
    for section, pattern in heading_patterns.items():
        regex = rf"(?im)^\s*(?:\d+(?:\.\d+)*\.?\s*)?(?:{pattern})\s*$"
        for match in re.finditer(regex, normalized):
            matches.append((match.start(), match.end(), section))

    matches.sort(key=lambda item: item[0])

    sections = {
        "abstract": "",
        "introduction": "",
        "methods": "",
        "results": "",
        "discussion": "",
        "conclusion": "",
    }

    for index, (_, heading_end, section) in enumerate(matches):
        if section == "references":
            continue

        next_start = len(normalized)
        for next_match in matches[index + 1:]:
            next_start = next_match[0]
            break

        content = normalized[heading_end:next_start].strip()
        if content and section in sections:
            sections[section] = content

    return sections
