from dataclasses import dataclass


@dataclass(frozen=True)
class LoadedDocument:
    content: str
    source: str
    page: int | None = None


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    source: str
    page: str
    distance: float | None = None

