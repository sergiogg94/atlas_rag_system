from pathlib import Path
from app.core.logging import logger
from app.services.parsers import DocumentParser
from typing import Optional, Tuple

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_document(file_path: Path) -> Tuple[bool, Optional[str]]:
    logger.info(f"Validating document: {file_path}")

    # Check if the file exists
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return False, "File not found."

    # Check if the file is a supported type
    alowed_files = DocumentParser().allowed_extensions
    if file_path.suffix.lower() not in alowed_files:
        logger.error(f"Unsupported file type: {file_path.suffix}")
        return False, f"Unsupported file type. Allowed types: {', '.join(alowed_files)}"

    # Check if the file size is within limits
    if file_path.stat().st_size > MAX_FILE_SIZE:
        logger.error(f"File size exceeds limit: {file_path.stat().st_size} bytes")
        return False, "File size exceeds the 10 MB limit."

    logger.info(f"Document validation passed")
    return True, None
