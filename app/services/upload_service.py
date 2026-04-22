from fastapi import UploadFile
from app.core.logging import logger
from app.core.exceptions import (
    DocumentValidationError,
    DocumentParsingError,
    UploadProcessError,
)
from app.services.rag_service import RAGService
from app.services.validators import validate_document
from app.services.parsers import DocumentParser
from pathlib import Path
import tempfile
import os
from typing import Optional


class UploadService:
    """Service for handling document uploads and ingestion."""

    def __init__(self):
        self.validator = validate_document
        self.parser = DocumentParser()

    async def process_upload(
        self,
        file: UploadFile,
        title: Optional[str] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
    ) -> dict:
        """Process an uploaded file and ingest it into the RAG system.

        Args:
            file (UploadFile): The uploaded file.
            title (Optional[str]): Optional title for the document. Defaults to filename.
            chunk_size (int): Size of text chunks for processing. Defaults to 500.
            chunk_overlap (int): Overlap between chunks. Defaults to 50.
            min_chunk_size (int): Minimum size for a chunk. Defaults to 100.

        Returns:
            dict: A dictionary containing the status and title of the ingested document.

        Raises:
            DocumentValidationError: If file validation fails.
            DocumentParsingError: If document parsing fails.
            UploadProcessError: If document ingestion fails.
        """
        logger.info(f"Upload document process started with file: {file.filename}")

        # Create a temporary directory and save the file
        temp_dir = tempfile.gettempdir()
        file_path = Path(temp_dir) / file.filename

        try:
            # Save the uploaded file to the temporary directory
            logger.info(f"Saving file to temporary location: {file_path}")
            with open(file_path, "wb") as temp_file:
                content = await file.read()
                temp_file.write(content)

            # Validate the document
            is_valid, error_message = self.validator(file_path)
            if not is_valid:
                logger.error(f"Document validation failed: {error_message}")
                raise DocumentValidationError(error_message)

            # Parse the document
            parsed_content = self.parser.parse(file_path)
            if parsed_content is None:
                logger.error("Failed to parse document")
                raise DocumentParsingError("Failed to parse the document.")

            # Use provided title or fall back to filename
            document_title = title or file.filename

            # Ingest the parsed content
            rag_service = RAGService(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                min_chunk_size=min_chunk_size,
            )
            await rag_service.ingest(title=document_title, content=parsed_content)

            logger.info(
                f"Document '{document_title}' uploaded and ingested successfully."
            )
            return {"status": "ok", "title": document_title}

        except DocumentValidationError:
            raise
        except DocumentParsingError:
            raise
        except Exception as e:
            logger.error(f"Error during document upload: {e}")
            raise UploadProcessError(str(e))

        finally:
            # Clean up the temporary file
            if file_path.exists():
                try:
                    os.remove(file_path)
                    logger.info(f"Temporary file removed: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file {file_path}: {e}")
