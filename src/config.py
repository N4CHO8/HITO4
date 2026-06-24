from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class RagSettings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    llm_model: str = os.getenv("OLLAMA_LLM_MODEL", "llama3.2:3b")
    vector_path: str = os.getenv("VECTOR_PATH", "data/faiss")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    top_k: int = int(os.getenv("TOP_K", "4"))
    max_context_distance: float = float(os.getenv("MAX_CONTEXT_DISTANCE", "0.35"))
