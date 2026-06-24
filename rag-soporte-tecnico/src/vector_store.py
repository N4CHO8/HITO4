from pathlib import Path
import json

import faiss
import numpy as np

from .schema import DocumentChunk, RetrievedChunk


class FaissVectorStore:
    def __init__(self, persist_path: str) -> None:
        self.persist_path = Path(persist_path)
        self.persist_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.persist_path / "index.faiss"
        self.metadata_path = self.persist_path / "chunks.json"
        self.index: faiss.Index | None = None
        self.chunks: list[dict[str, object]] = []
        self._load()

    def reset(self) -> None:
        self.index = None
        self.chunks = []
        for path in (self.index_path, self.metadata_path):
            if path.exists():
                path.unlink()

    def upsert(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return

        vectors = np.array(embeddings, dtype="float32")
        faiss.normalize_L2(vectors)

        if self.index is None:
            self.index = faiss.IndexFlatIP(vectors.shape[1])

        self.index.add(vectors)
        for chunk in chunks:
            self.chunks.append(
                {
                    "id": chunk.id,
                    "text": chunk.text,
                    "metadata": chunk.metadata,
                }
            )
        self._save()

    def count(self) -> int:
        return len(self.chunks)

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        if self.index is None or not self.chunks:
            return []

        vector = np.array([embedding], dtype="float32")
        faiss.normalize_L2(vector)
        scores, indexes = self.index.search(vector, min(top_k, len(self.chunks)))

        retrieved: list[RetrievedChunk] = []
        for score, index in zip(scores[0], indexes[0]):
            if index < 0:
                continue
            item = self.chunks[int(index)]
            metadata = item["metadata"]
            retrieved.append(
                RetrievedChunk(
                    text=str(item["text"]),
                    source=str(metadata.get("source", "desconocido")),
                    page=str(metadata.get("page", "")),
                    distance=1.0 - float(score),
                )
            )
        return retrieved

    def _load(self) -> None:
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self.chunks = json.loads(self.metadata_path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        if self.index is not None:
            faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(
            json.dumps(self.chunks, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
