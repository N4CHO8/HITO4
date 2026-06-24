from hashlib import sha1
import re

from .schema import DocumentChunk, LoadedDocument


def chunk_text(text: str, max_chars: int = 900, overlap: int = 150) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars debe ser mayor a 0")
    if overlap < 0 or overlap >= max_chars:
        raise ValueError("overlap debe ser mayor o igual a 0 y menor que max_chars")

    clean_text = normalize_text(text)
    if not clean_text:
        return []

    paragraphs = re.split(r"\n\s*\n", clean_text)
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(paragraph) > max_chars:
            if current:
                chunks.append(current.strip())
                current = ""
            chunks.extend(split_long_text(paragraph, max_chars, overlap))
            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
        else:
            chunks.append(current.strip())
            prefix = current[-overlap:].strip() if overlap and current else ""
            current = f"{prefix}\n\n{paragraph}".strip() if prefix else paragraph

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_documents(
    documents: list[LoadedDocument],
    max_chars: int = 900,
    overlap: int = 150,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for document in documents:
        for index, text in enumerate(chunk_text(document.content, max_chars, overlap), start=1):
            page = str(document.page or "")
            digest = sha1(f"{document.source}:{page}:{index}:{text}".encode("utf-8")).hexdigest()
            chunks.append(
                DocumentChunk(
                    id=digest,
                    text=text,
                    metadata={
                        "source": document.source,
                        "page": page,
                        "chunk": str(index),
                    },
                )
            )
    return chunks


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_long_text(text: str, max_chars: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

