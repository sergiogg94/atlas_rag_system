import pytest
from app.services.chunking import TextChunker


@pytest.fixture
def chunker():
    return TextChunker()


@pytest.fixture
def custom_chunker():
    return TextChunker(chunk_size=100, chunk_overlap=20)


# Tests for chunk_text
def test_chunk_text_basic(chunker):
    text = "This is a test. " * 5000
    chunks = chunker.chunk_text(text)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_chunk_text_empty_string(chunker):
    chunks = chunker.chunk_text("")
    assert chunks == []


def test_chunk_text_whitespace_only(chunker):
    chunks = chunker.chunk_text("   \n\t  ")
    assert chunks == []


def test_chunk_text_short_text(chunker):
    text = "Short text"
    chunks = chunker.chunk_text(text)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_respects_chunk_size(custom_chunker):
    text = "word " * 200
    chunks = custom_chunker.chunk_text(text)

    for chunk in chunks:
        assert len(chunk) <= custom_chunker.chunk_size + 50


def test_chunk_text_with_separators():
    text = "Para 1.\n\nPara 2.\n\nPara 3." * 20
    chunker = TextChunker(chunk_size=100, separators=["\n\n"])
    chunks = chunker.chunk_text(text)

    assert len(chunks) > 0
    # Verify chunks are created
    assert sum(len(chunk) for chunk in chunks) > 0


def test_chunk_text_preserves_content(chunker):
    text = "The quick brown fox jumps over the lazy dog. " * 20
    chunks = chunker.chunk_text(text)
    joined = "".join(chunks)

    assert text in joined or joined.strip() == text.strip()


# Tests for get_chunk_stats
def test_get_chunk_stats_basic(chunker):
    chunks = ["Hello world", "This is a test", "Another chunk here"]
    stats = chunker.get_chunk_stats(chunks)

    assert "total_chunks" in stats
    assert "avg_length" in stats
    assert "min_length" in stats
    assert "max_length" in stats
    assert "total_chars" in stats

    assert stats["total_chunks"] == 3
