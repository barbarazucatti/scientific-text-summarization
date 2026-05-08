import tempfile
from pathlib import Path

import streamlit as st

from main import process_article


st.set_page_config(
    page_title="Leitura Cientifica Guiada",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #272321;
            --muted: #6f6761;
            --paper: #fffaf1;
            --line: #e7dccb;
            --mint: #cfe6cf;
            --blue: #cbe3e6;
            --pink: #f5c8cf;
            --yellow: #f7df93;
            --coral: #ed765f;
        }

        .stApp {
            background:
                linear-gradient(rgba(231, 220, 203, 0.42) 1px, transparent 1px),
                linear-gradient(90deg, rgba(231, 220, 203, 0.42) 1px, transparent 1px),
                var(--paper);
            background-size: 26px 26px;
            color: var(--ink);
        }

        .block-container {
            max-width: 1040px;
            padding-top: 2.25rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, span, div {
            letter-spacing: 0;
        }

        .top-strip {
            height: 10px;
            border: 1px solid var(--ink);
            background: repeating-linear-gradient(
                90deg,
                var(--mint) 0 22px,
                var(--blue) 22px 44px,
                var(--yellow) 44px 66px,
                var(--pink) 66px 88px
            );
            margin-bottom: 18px;
        }

        .hero {
            border: 1px solid var(--ink);
            background: rgba(255, 250, 241, 0.86);
            padding: 30px 34px 24px;
            box-shadow: 6px 6px 0 #272321;
        }

        .eyebrow {
            display: inline-block;
            border: 1px solid var(--ink);
            background: var(--blue);
            padding: 5px 10px;
            font-size: 0.76rem;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 18px;
        }

        .hero h1 {
            font-size: clamp(2.35rem, 6vw, 5.3rem);
            line-height: 0.92;
            margin: 0 0 18px;
            color: var(--ink);
            max-width: 760px;
        }

        .hero p {
            max-width: 720px;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
        }

        .workbench {
            border: 1px solid var(--ink);
            background: rgba(255, 255, 255, 0.72);
            padding: 22px;
            margin-top: 22px;
        }

        .guide-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin: 22px 0;
        }

        .guide-card {
            border: 1px solid var(--ink);
            background: #fffdf8;
            padding: 16px;
            min-height: 124px;
        }

        .guide-card:nth-child(1) { background: var(--blue); }
        .guide-card:nth-child(2) { background: var(--pink); }
        .guide-card:nth-child(3) { background: var(--mint); }

        .guide-card strong {
            display: block;
            font-size: 0.86rem;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .guide-card p {
            color: var(--ink);
            font-size: 0.92rem;
            line-height: 1.45;
            margin: 0;
        }

        .note {
            border-left: 5px solid var(--coral);
            background: #fffdf8;
            padding: 14px 16px;
            color: var(--muted);
            line-height: 1.5;
            margin: 16px 0 4px;
        }

        .result-wrap {
            border: 1px solid var(--ink);
            background: #fffdf8;
            padding: 24px;
            margin-top: 24px;
        }

        .stButton > button {
            border: 1px solid var(--ink);
            background: var(--coral);
            color: white;
            border-radius: 999px;
            padding: 0.65rem 1.1rem;
            font-weight: 700;
        }

        .stButton > button:hover {
            border: 1px solid var(--ink);
            background: #d85f49;
            color: white;
        }

        [data-testid="stFileUploader"] {
            background: #fffdf8;
            border: 1px dashed var(--ink);
            padding: 14px;
        }

        @media (max-width: 760px) {
            .hero {
                padding: 24px 20px;
                box-shadow: 4px 4px 0 #272321;
            }

            .guide-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="top-strip"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
        <span class="eyebrow">apoio de leitura</span>
        <h1>Leitura Cient&iacute;fica Guiada</h1>
        <p>
            Use esta p&aacute;gina para ler um artigo com mais clareza. Ela prepara uma explica&ccedil;&atilde;o
            em portugu&ecirc;s brasileiro, mantendo as cautelas do estudo e separando o que foi observado
            do que ainda n&atilde;o d&aacute; para afirmar.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="guide-grid">
        <div class="guide-card">
            <strong>1. PDF</strong>
            <p>Escolha um artigo cient&iacute;fico. Pode estar em ingl&ecirc;s ou portugu&ecirc;s.</p>
        </div>
        <div class="guide-card">
            <strong>2. Leitura</strong>
            <p>O texto &eacute; analisado com foco no objetivo, nos achados e nas limita&ccedil;&otilde;es.</p>
        </div>
        <div class="guide-card">
            <strong>3. Explica&ccedil;&atilde;o</strong>
            <p>Voc&ecirc; recebe um resumo curto, conceitos importantes e cuidados para n&atilde;o exagerar.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="workbench">', unsafe_allow_html=True)
st.subheader("Selecionar artigo")
st.write(
    "Carregue um PDF com texto selecionavel. Arquivos scaneados como imagem podem nao ser lidos corretamente."
)

uploaded_file = st.file_uploader(
    "Arquivo PDF",
    type="pdf",
    label_visibility="collapsed",
)

st.markdown(
    """
    <div class="note">
        O resultado serve como guia inicial de leitura. Para decisoes importantes, confira o artigo original
        e observe especialmente metodo, amostra, resultados e limitacoes.
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is not None:
    st.write(f"Arquivo selecionado: {uploaded_file.name}")

    if st.button("Gerar leitura guiada", type="primary"):
        suffix = Path(uploaded_file.name).suffix or ".pdf"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        try:
            with st.spinner("Lendo o artigo e organizando a explicacao..."):
                result = process_article(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)

        st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
        st.markdown("### Leitura guiada")
        st.markdown(result)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
