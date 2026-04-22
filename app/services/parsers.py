from pathlib import Path
import fitz  # PyMuPDF
from app.core.logging import logger
from typing import Optional


class DocumentParser:
    """Parser for documents to text."""

    def __init__(self):
        self.allowed_extensions = [".txt", ".pdf", ".md"]

    @staticmethod
    def parse_txt(file_path: Path) -> str:
        """Parse a text file and return its content.

        Args:
            file_path (Path): Path to the text file.

        Returns:
            str: Content of the text file.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def parse_pdf(file_path: Path) -> str:
        """Parse a PDF file and return its text content.

        Args:
            file_path (Path): Path to the PDF file.

        Returns:
            str: Text content of the PDF file.
        """
        text_content = []

        with fitz.open(file_path) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text_content.append(page_text)

        return "\n".join(text_content).strip()

    def parse(self, file_path: Path) -> Optional[str]:
        """Parse a document based on its file extension.
        Args:
            file_path (Path): Path to the document file.
        Returns:
            Optional[str]: Parsed text content of the document, or None if parsing fails.
        """
        suffix = file_path.suffix.lower()

        if suffix not in self.allowed_extensions:
            logger.error(f"Unsupported file type: {suffix}")
            return None

        parsers = {
            ".txt": DocumentParser.parse_txt,
            ".pdf": DocumentParser.parse_pdf,
            ".md": DocumentParser.parse_txt,
        }
        parser_func = parsers.get(suffix)

        try:
            return parser_func(file_path)
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            return None
