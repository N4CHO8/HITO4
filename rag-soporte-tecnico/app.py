import streamlit as st

from src.rag import RagAssistant


st.set_page_config(page_title="Asistente RAG de Soporte Tecnico")

st.title("Asistente RAG de Soporte Tecnico")

with st.sidebar:
    st.header("Configuracion")
    docs_dir = st.text_input("Directorio de documentos", value="docs")
    reset = st.checkbox("Recrear base vectorial", value=False)
    if st.button("Indexar documentos"):
        with st.spinner("Generando embeddings e indexando documentos..."):
            assistant = RagAssistant()
            total = assistant.ingest(docs_dir, reset=reset)
            st.success(f"Indexacion completada: {total} fragmentos.")

    st.caption("Modelos por defecto: nomic-embed-text + llama3.2:3b")

question = st.text_area(
    "Pregunta",
    value="Como crear una imagen Docker?",
    height=100,
)

if st.button("Preguntar"):
    with st.spinner("Recuperando contexto y generando respuesta..."):
        assistant = RagAssistant()
        result = assistant.ask(question)

    st.subheader("Respuesta")
    st.write(result["answer"])

    st.subheader("Fuentes utilizadas")
    for source in result["sources"]:
        st.write(f"- {source}")

    st.subheader("Fragmentos recuperados")
    for index, chunk in enumerate(result["retrieved"], start=1):
        label = f"{index}. {chunk.source}"
        if chunk.page:
            label += f" pagina {chunk.page}"
        with st.expander(label):
            st.write(chunk.text)
            if chunk.distance is not None:
                st.caption(f"Distancia vectorial: {chunk.distance:.4f}")
