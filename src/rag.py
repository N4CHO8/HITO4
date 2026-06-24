from pathlib import Path

from .chunker import chunk_documents
from .config import RagSettings
from .document_loader import load_documents
from .ollama_client import OllamaClient
from .schema import RetrievedChunk
from .vector_store import FaissVectorStore


class RagAssistant:
    def __init__(self, settings: RagSettings | None = None) -> None:
        self.settings = settings or RagSettings()
        self.ollama = OllamaClient(
            base_url=self.settings.ollama_base_url,
            embedding_model=self.settings.embedding_model,
            llm_model=self.settings.llm_model,
        )
        self.store = FaissVectorStore(persist_path=self.settings.vector_path)

    def ingest(self, docs_dir: str | Path, reset: bool = False) -> int:
        if reset:
            self.store.reset()

        documents = load_documents(docs_dir)
        chunks = chunk_documents(
            documents,
            max_chars=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )
        embeddings = self.ollama.embed([chunk.text for chunk in chunks])
        self.store.upsert(chunks, embeddings)
        return len(chunks)

    def ask(self, question: str) -> dict[str, object]:
        question = question.strip()
        if not question:
            raise ValueError("La pregunta no puede estar vacia.")

        query_embedding = self.ollama.embed_one(question)
        retrieved = self.store.query(query_embedding, self.settings.top_k)
        if is_out_of_context(retrieved, self.settings.max_context_distance):
            return {
                "question": question,
                "answer": "No encontre informacion suficiente en los documentos para responder esa pregunta.",
                "sources": [],
                "retrieved": retrieved,
            }

        context_chunks = filter_context(retrieved, self.settings.max_context_distance)
        prompt = build_prompt(question, context_chunks)
        answer = self.ollama.generate_answer(prompt)
        return {
            "question": question,
            "answer": answer,
            "sources": format_sources(context_chunks),
            "retrieved": retrieved,
        }


def build_prompt(question: str, retrieved: list[RetrievedChunk]) -> str:
    context_blocks = []
    for index, chunk in enumerate(retrieved, start=1):
        page = f", pagina {chunk.page}" if chunk.page else ""
        context_blocks.append(
            f"[Fuente {index}: {chunk.source}{page}]\n{chunk.text}"
        )

    context = "\n\n---\n\n".join(context_blocks)
    return f"""
Eres un asistente de soporte tecnico. Responde en espanol claro y breve.
Usa exclusivamente el CONTEXTO RECUPERADO. Si la respuesta no esta en el
contexto, responde: "No encontre informacion suficiente en los documentos para
responder esa pregunta." No inventes procedimientos.

No incluyas enlaces ni bibliografia dentro de la respuesta; la aplicacion
mostrara las fuentes recuperadas por separado.

PREGUNTA:
{question}

CONTEXTO RECUPERADO:
{context}
""".strip()


def format_sources(retrieved: list[RetrievedChunk]) -> list[str]:
    sources: list[str] = []
    for chunk in retrieved:
        label = chunk.source
        if chunk.page:
            label = f"{label}, pagina {chunk.page}"
        if label not in sources:
            sources.append(label)
    return sources


def is_out_of_context(retrieved: list[RetrievedChunk], max_distance: float) -> bool:
    if not retrieved:
        return True
    best_distance = retrieved[0].distance
    return best_distance is None or best_distance > max_distance


def filter_context(
    retrieved: list[RetrievedChunk],
    max_distance: float,
) -> list[RetrievedChunk]:
    return [
        chunk
        for chunk in retrieved
        if chunk.distance is not None and chunk.distance <= max_distance
    ]
