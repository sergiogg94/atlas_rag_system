from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """Utility class for chunking text into manageable pieces for RAG processing."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] = None,
        length_function: callable = len,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if separators is None:
            separators = [
                "\n\n",
                "\n",
                ". ",
                "! ",
                "? ",
                "; ",
                ", ",
                " ",
                "",
            ]

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=length_function,
            is_separator_regex=False,
        )

    def chunk_text(self, text: str) -> List[str]:
        """Creates chunks from the input text using the configured text splitter.

        Args:
            text (str): The input text to be chunked.

        Returns:
            List[str]: A list of text chunks generated from the input text.
        """
        if not text.strip():
            return []
        return self.text_splitter.split_text(text)

    def get_chunk_stats(self, chunks: List[str]) -> dict:
        """Generates statistics about chunks.

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
