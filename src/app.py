import tempfile
from pathlib import Path

import streamlit as st

from main import process_article


MAX_PDF_SIZE_MB = 10
MAX_PDF_SIZE_BYTES = MAX_PDF_SIZE_MB * 1024 * 1024


st.set_page_config(
    page_title="Insight Cientifico",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #272321;
            --muted: #6f6761;
            --paper: #fffdf7;
            --line: #c9dff0;
            --margin: #f0b3aa;
            --mint: #dcebd8;
            --blue: #d7edf7;
            --pink: #f5d7dc;
            --yellow: #f6e8b8;
            --coral: #d96f5d;
        }

        .stApp {
            background:
                linear-gradient(90deg, transparent 0 72px, rgba(240, 179, 170, 0.45) 72px 73px, transparent 73px),
                repeating-linear-gradient(0deg, var(--paper) 0 31px, rgba(201, 223, 240, 0.68) 31px 32px);
            color: var(--ink);
        }

        .block-container {
            max-width: 980px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, span, div {
            letter-spacing: 0;
        }

        .hero {
            background: rgba(255, 253, 247, 0.72);
            padding: 18px 0 8px;
        }

        .eyebrow {
            display: inline-block;
            border-bottom: 2px solid var(--margin);
            color: var(--muted);
            padding: 0 0 4px;
            font-size: 0.76rem;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .hero h1 {
            font-size: clamp(2.2rem, 5vw, 4rem);
            line-height: 1;
            margin: 0 0 14px;
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

        .workbench-title {
            margin-top: 1.4rem;
            margin-bottom: 0.2rem;
            font-size: 0.92rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--muted);
        }

        .guide-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin: 20px 0 24px;
        }

        .guide-card {
            border: 1px solid rgba(39, 35, 33, 0.28);
            background: #fffdf8;
            padding: 16px;
            min-height: 124px;
            box-shadow: 0 8px 18px rgba(39, 35, 33, 0.08);
        }

        .guide-card:nth-child(1) { background: var(--blue); transform: rotate(-0.7deg); }
        .guide-card:nth-child(2) { background: var(--yellow); transform: rotate(0.6deg); }
        .guide-card:nth-child(3) { background: var(--mint); transform: rotate(-0.35deg); }

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
            margin: 16px 0 10px;
        }

        .stButton > button {
            border: 1px solid rgba(39, 35, 33, 0.32);
            background: var(--coral);
            color: white;
            border-radius: 999px;
            padding: 0.65rem 1.1rem;
            font-weight: 700;
        }

        .stButton > button:hover {
            border: 1px solid rgba(39, 35, 33, 0.32);
            background: #d85f49;
            color: white;
        }

        [data-testid="stFileUploader"] {
            background: #fffdf8;
            border: 1px dashed rgba(39, 35, 33, 0.36);
            padding: 14px;
        }

        @media (max-width: 760px) {
            .hero {
                padding: 18px 0 8px;
            }

            .guide-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <span class="eyebrow">apoio de leitura</span>
        <h1>Insight Cient&iacute;fico</h1>
        <p>
            Use esta p&aacute;gina para ler um artigo com mais clareza. Ela prepara uma explica&ccedil;&atilde;o
            em portugu&ecirc;s, mantendo as cautelas do estudo e separando o que foi observado
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

st.markdown('<h2 class="workbench-title">Selecionar artigo</h2>', unsafe_allow_html=True)
st.write(
    f"Carregue um PDF com texto selecionável, de até {MAX_PDF_SIZE_MB} MB. Arquivos scaneados como imagem podem não ser lidos corretamente."
)

uploaded_file = st.file_uploader(
    "Arquivo PDF",
    type="pdf",
    label_visibility="collapsed",
)

st.markdown(
    """
    <div class="note">
        O insight serve como apoio inicial de leitura. Ele não substitui o artigo original:
        confira método, amostra, resultados e limitações antes de usar a informação em decisões importantes.
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.write(f"Arquivo selecionado: {uploaded_file.name} ({file_size_mb:.1f} MB)")

    file_is_too_large = uploaded_file.size > MAX_PDF_SIZE_BYTES
    if file_is_too_large:
        st.warning(
            f"Este PDF tem {file_size_mb:.1f} MB. Envie um arquivo de até {MAX_PDF_SIZE_MB} MB para gerar o insight."
        )

    if st.button("Gerar insight científico", type="primary", disabled=file_is_too_large):
        suffix = Path(uploaded_file.name).suffix or ".pdf"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        try:
            with st.spinner("Lendo o artigo e organizando a explicacao..."):
                result = process_article(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)

        st.markdown("### Insight cientifico")
        st.markdown(result)
