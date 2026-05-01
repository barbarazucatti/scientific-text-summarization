import re

def clean_text(text):
    # 1. remover quebras de linha
    text = text.replace("\n", " ")

    # 2. remover URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # 3. separar palavras coladas (camelCase)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # 4. corrigir palavras quebradas tipo "fi ef cacy"
    text = re.sub(r'(\b\w{1,2})\s+(\w{1,2})\s+(\w+)', r'\1\2\3', text)

    # 5. remover números soltos de autores (ex: Tao Lei1,8)
    text = re.sub(r'\d+(,\d+)*', '', text)

    # 6. remover palavras em caixa alta muito curtas (tipo headers)
    text = re.sub(r'\b[A-Z]{2,}\b', '', text)

    # 7. remover espaços duplicados
    text = re.sub(r'\s+', ' ', text)

    return text.strip()