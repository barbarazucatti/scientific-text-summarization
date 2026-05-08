# Scientific Text Summarization - Insight Científico

Aplicação em Streamlit que utiliza Large Language Models (LLMs) para transformar artigos científicos complexos em explicações claras, acessíveis e fáceis de entender.

A ferramenta extrai conteúdo de PDFs científicos, identifica seções relevantes do artigo e gera:
- resumos simplificados,
- explicações em linguagem natural,
- conceitos-chave,
- e contextualizações para facilitar a compreensão técnica.

O projeto foi desenvolvido como um protótipo de IA aplicada à democratização do conhecimento científico, explorando técnicas de:
- processamento de PDFs,
- limpeza e estruturação de texto,
- chunking inteligente,
- sumarização com LLMs,
- e interface interativa com Streamlit.

## O que o app faz

- Upload de artigos científicos em PDF
- Extração automática de texto
- Limpeza e pré-processamento do conteúdo
- Chunking inteligente para processamento com LLM
- Explicações simplificadas em linguagem natural
- Extração de conceitos-chave
- Interface interativa com Streamlit

## Como rodar

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

Antes de rodar, configure sua chave da OpenAI:

```bash
set OPENAI_API_KEY=sua-chave-aqui
```

No PowerShell:

```powershell
$env:OPENAI_API_KEY="sua-chave-aqui"
```

## Objetivo

Democratizar o acesso ao conhecimento cientifico, explicando pesquisas complexas com clareza, fidelidade e responsabilidade.
