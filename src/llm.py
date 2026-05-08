import os

from openai import OpenAI

MODEL = "gpt-4o-mini"


def _get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def _get_client():
    api_key = _get_api_key()
    if api_key:
        return OpenAI(api_key=api_key)

    return OpenAI()


def _extract_response_text(response):
    return response.output[0].content[0].text


def simplify_text(text):
    print(">>> Texto recebido pelo LLM:")
    print(repr(text[:1000]))

    prompt = f"""
Voce e um tradutor cientifico responsavel para portugues brasileiro.

Sua tarefa e transformar o texto fornecido de um artigo cientifico em um resumo amigavel, curto e acessivel para pessoas leigas.

O texto pode estar em ingles, portugues ou outro idioma.
Leia o texto no idioma original, mas responda sempre em portugues brasileiro.

REGRAS OBRIGATORIAS:
- Use somente informacoes presentes no texto fornecido.
- Se o texto indicar que um trecho foi omitido para reduzir tempo, nao tente preencher essa lacuna.
- Nao adicione contexto externo.
- Nao invente aplicacoes, promessas, tratamentos ou conclusoes.
- Nao transforme hipotese em fato.
- Nao transforme resultados em animais, celulas ou laboratorio em resultado comprovado em humanos.
- Nao use palavras como "cura", "revolucionario", "definitivo" ou "comprovado" se o texto nao afirmar isso claramente.
- Preserve o grau de certeza dos autores.
- Se o texto disser "pode", "sugere", "foi observado", "em camundongos", "em celulas" ou "estudo preliminar", mantenha essa cautela.
- Se uma informacao importante nao estiver clara, diga: "O artigo nao informa isso com clareza."

PROCESSO:
1. Extraia os fatos principais do artigo.
2. Escolha apenas o que e mais importante para uma pessoa leiga entender a ideia central.
3. Revise a explicacao final e remova qualquer afirmacao que nao esteja apoiada no texto.

ESTILO DO RESUMO:
- Escreva primeiro um unico paragrafo curto, com 4 a 6 frases.
- O tom deve parecer divulgacao cientifica simples, nao relatorio tecnico.
- Comece com "O artigo..." quando isso soar natural.
- Foque no problema estudado, na proposta principal, no possivel impacto e na cautela.
- Nao liste detalhes secundarios no paragrafo principal, como orgaos reguladores, numeros de produtos aprovados, nomes de aprovacao, custos ou processo industrial, a menos que sejam a descoberta central do artigo.
- Prefira frases como "mostra potencial", "pode ajudar", "ainda precisa de mais estudos" quando o artigo nao trouxer certeza forte.

Texto:
{text}

Responda exatamente neste formato:

### Resumo do artigo
Um unico paragrafo curto, amigavel e claro, como divulgacao cientifica responsavel.

### Principais informações do estudo:
- Problema investigado:
- Objetivos dos pesquisadores:
- O que foi realizado no estudo:
- Principais descobertas:
- Possíveis impactos ou aplicações:
- O que o estudo ainda não permite concluir:

### Conceitos importantes:
- Termo: explicacao simples
- Termo: explicacao simples
- Termo: explicacao simples

### Cuidado:
- Liste as principais limitacoes, incertezas ou cautelas do artigo.
"""

    response = _get_client().responses.create(
        model=MODEL,
        input=prompt
    )

    return _extract_response_text(response)


def merge_summaries(summaries):
    if not summaries:
        return "Nao foi possível gerar a explição porque nenhum texto útil foi extraído do PDF."

    prompt = f"""
Você está juntando explicações parciais de um mesmo artigo científico.

Sua tarefa e produzir uma explicacao final em portugues brasileiro para pessoas leigas.

REGRAS OBRIGATORIAS:
- Use apenas informacoes presentes nos resumos abaixo.
- Nao adicione informacoes novas.
- Remova repeticoes.
- Preserve cautelas, limitacoes e incertezas.
- Nao aumente o grau de certeza dos resultados.
- Nao transforme pesquisa preliminar em tratamento disponivel.
- Se houver conflito entre os resumos, mencione que a informacao nao esta clara.

Resumos parciais:
{chr(10).join(summaries)}

Responda exatamente neste formato:

### Resumo do artigo:
Um texto corrido, amigavel e claro.

### Principais informações do estudo:
- Problema investigado:
- Objetivos dos pesquisadores:
- O que foi realizado no estudo:
- Principais descobertas:
- Possíveis impactos ou aplicações:
- O que o estudo ainda não permite concluir:

### Conceitos importantes:
- Termo: explicacao simples

### Cuidado:
- Limitacoes e cautelas principais.
"""

    response = _get_client().responses.create(
        model=MODEL,
        input=prompt
    )

    return _extract_response_text(response)
