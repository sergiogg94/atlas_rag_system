"""Custom exceptions for the RAG service."""


class DocumentValidationError(Exception):
    """Raised when document validation fails."""

    pass


class DocumentParsingError(Exception):
    """Raised when document parsing fails."""

    pass


class UploadProcessError(Exception):
    """Raised when document upload/ingestion process fails."""

    pass
