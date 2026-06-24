import pytest

from src.chunker import chunk_text


def test_chunk_text_keeps_small_text_in_one_chunk():
    chunks = chunk_text("Linea uno.\n\nLinea dos.", max_chars=100, overlap=10)

    assert chunks == ["Linea uno.\n\nLinea dos."]


def test_chunk_text_splits_long_text_with_overlap():
    text = "A" * 50 + "\n\n" + "B" * 50 + "\n\n" + "C" * 50
    chunks = chunk_text(text, max_chars=80, overlap=10)

    assert len(chunks) >= 2
    assert all(len(chunk) <= 90 for chunk in chunks)


def test_chunk_text_validates_overlap():
    with pytest.raises(ValueError):
        chunk_text("texto", max_chars=100, overlap=100)

