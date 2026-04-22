from typing import List
import re


class TextChunker:
    """Utility class for chunking text into manageable pieces for RAG processing."""

    def __init__(
        self, chunk_size: int = 500, chunk_overlap: int = 50, min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def clean_text(self, text: str) -> str:
        """Clean text to remove aditional spaces and newlines.

        Args:
            text (str): Text to clean.

        Returns:
            str: Cleaned text.
        """
        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)
        # Remove multiple newlines
        text = re.sub(r"\n+", "\n", text)
        return text.strip()

    def chunk_by_characters(self, text: str) -> List[str]:
        """Chunk text by character count, trying to break at sentence boundaries when possible.

        Args:
            text (str): Text to chunk.

        Returns:
            List[str]: List of text chunks.
        """
        text = self.clean_text(text)
        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < text_length:
                # Look for period, question mark, or exclamation
                boundary = text.rfind(".", start, end)
                if boundary == -1:
                    boundary = text.rfind("?", start, end)
                if boundary == -1:
                    boundary = text.rfind("!", start, end)

                if boundary != -1 and boundary > start + self.min_chunk_size:
                    end = boundary + 1

            chunk = text[start:end].strip()

            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)

            # Move start with overlap
            start = end - self.chunk_overlap

        return chunks

    def get_chunk_stats(self, chunks: List[str]) -> dict:
        """Generates statistics abput chunks.

        Args:
            chunks (List[str]): List of text chunks.

        Returns:
            dict: A dictionary containing statistics about the chunks.
        """
        if not chunks:
            return {}

        lengths = [len(c) for c in chunks]
        return {
            "total_chunks": len(chunks),
            "avg_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_chars": sum(lengths),
        }
