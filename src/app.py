import streamlit as st
from main import process_article

st.markdown("""
<style>
    .main {
        background-color: #f7f7f7;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Scientific Simplifier",
    layout="wide"
)

# 🌿 Header
st.title("🧠 Scientific Article Simplifier")
st.caption("Turn complex research into clear explanations")

st.divider()

# 📂 Upload
uploaded_file = st.file_uploader(
    "Upload a scientific paper (PDF)",
    type="pdf"
)

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("✨ Simplify"):
        with st.spinner("Reading and simplifying the article..."):
            result = process_article("temp.pdf")

        st.divider()

        # 🧠 Resultado em coluna centralizada
        col1, col2, col3 = st.columns([1, 6, 1])

        with col2:
    # separa as seções do texto
            if "### Key Concepts Explained:" in result:
                simplified, concepts = result.split("### Key Concepts Explained:")
            else:
                simplified = result
                concepts = ""

            # 🧠 explicação principal
            st.markdown("### 🧠 Simplified Explanation")
            st.markdown(simplified)

            # 🔬 conceitos em dropdown (expander)
            if concepts:
                with st.expander("🔬 Key Concepts Explained"):
                    st.markdown(concepts)