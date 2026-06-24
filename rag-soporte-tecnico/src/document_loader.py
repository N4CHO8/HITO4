from pathlib import Path

from pypdf import PdfReader

from .schema import LoadedDocument


SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


def load_documents(docs_dir: str | Path) -> list[LoadedDocument]:
    root = Path(docs_dir)
    if not root.exists():
        raise FileNotFoundError(f"No existe el directorio de documentos: {root}")

    documents: list[LoadedDocument] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        documents.extend(load_single_document(path, root))
    return documents


def load_single_document(path: Path, root: Path | None = None) -> list[LoadedDocument]:
    source = str(path.relative_to(root)) if root else path.name
    suffix = path.suffix.lower()

    if suffix in {".md", ".txt"}:
        return [
            LoadedDocument(
                content=path.read_text(encoding="utf-8"),
                source=source,
            )
        ]

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages: list[LoadedDocument] = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(LoadedDocument(content=text, source=source, page=index))
        return pages

    return []

