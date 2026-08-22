from pathlib import Path
from typing import Any

import httpx


class AtlasAPIClient:
    """Client for interacting with the Atlas API"""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "http://localhost:8000"
        self.timeout = 300.0

    async def health_check(self) -> dict[str, Any]:
        """Check the health status of the Atlas API"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()

    async def list_collections(self) -> list[dict]:
        """List all available collections"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/collections")
            response.raise_for_status()
            return response.json()["collections"]

    async def create_collection(
        self,
        name: str,
        provider: str,
        model: str,
        dimension: int,
        description: str = "",
    ) -> dict:
        """Creates a new vector collection"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/collections",
                json={
                    "name": name,
                    "provider": provider,
                    "model": model,
                    "dimension": dimension,
                    "description": description,
                },
            )
            response.raise_for_status()
            return response.json()

    async def delete_collection(self, collection_id: int) -> None:
        """Elimina una colección."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(
                f"{self.base_url}/collections/{collection_id}"
            )
            response.raise_for_status()

    async def get_provider_catalog(self) -> dict:
        """Obtiene el catálogo de proveedores y modelos disponibles."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/collections/catalog")
            response.raise_for_status()
            return response.json()["catalog"]

    async def query(
        self,
        question: str,
        collection_id: int,
        top_k: int = 5,
        max_distance: float = 1.0,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> dict[str, Any]:
        """Query the RAG system with a question and receive an answer along with source metadata."""
        payload = {
            "question": question,
            "collection_id": collection_id,
            "top_k": top_k,
            "max_distance": max_distance,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        # TODO: refactor for not repeat this code
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/query",
                json=payload,
            )

            response.raise_for_status()
            return response.json()

    async def ingest_document(
        self,
        title: str,
        content: str,
        collection_id: int,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> dict[str, Any]:
        """Ingest a single document into the RAG system by providing its title and content."""
        payload = {
            "title": title,
            "content": content,
            "collection_id": collection_id,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/ingest",
                json=payload,
            )

            response.raise_for_status()
            return response.json()

    async def upload_document(
        self,
        file_path: str,
        collection_id: int,
        title: str | None = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> dict[str, Any]:
        """Ingest a single document into the RAG system by uploading a file"""
        f_path = Path(file_path)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with open(f_path, "rb") as f:  # noqa: ASYNC230
                response = await client.post(
                    f"{self.base_url}/upload",
                    files={"file": (f_path.name, f)},
                    data={
                        "title": title,
                        "collection_id": collection_id,
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                    },
                )

                response.raise_for_status()
                return response.json()

    async def upload_batch(
        self,
        file_paths: list[str],
        collection_id: int,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> list[dict[str, Any]]:
        """Ingest multiple documents into the RAG system by uploading a batch of files"""
        results = []

        for file_path in file_paths:
            try:
                result = await self.upload_document(
                    file_path=file_path,
                    title=None,
                    collection_id=collection_id,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
                results.append(
                    {
                        "file": Path(file_path).name,
                        "status": "success",
                        "data": result,
                    }
                )
            except Exception as e:  # noqa: BLE001
                results.append(
                    {
                        "file": Path(file_path).name,
                        "status": "error",
                        "error": str(e),
                    }
                )
        return results

    async def search(
        self,
        query: str,
        collection_id: int,
        top_k: int = 5,
        max_distance: float = 1.0,
    ):
        """Search for relevant documents in the RAG system based on a query"""
        payload = {
            "query": query,
            "collection_id": collection_id,
            "top_k": top_k,
            "max_distance": max_distance,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/search",
                json=payload,
            )

            response.raise_for_status()
            return response.json()
