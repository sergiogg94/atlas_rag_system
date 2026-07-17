import httpx
from typing import Optional, List, Dict, Any
from pathlib import Path


class AtlasAPIClient:
    """Client for interacting with the Atlas API"""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or "http://localhost:8000"
        self.timeout = 300.0

    async def health_check(self) -> Dict[str, Any]:
        """Check the health status of the Atlas API"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()

    async def query(
        self,
        question: str,
        top_k: int = 5,
        probes: int = 10,
        max_distance: float = 1.0,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """Query the RAG system with a question and receive an answer along with source metadata."""
        payload = {
            "question": question,
            "top_k": top_k,
            "probes": probes,
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
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> Dict[str, Any]:
        """Ingest a single document into the RAG system by providing its title and content."""
        payload = {
            "title": title,
            "content": content,
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
        title: Optional[str] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> Dict[str, Any]:
        """Ingest a single document into the RAG system by uploading a file"""
        f_path = Path(file_path)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with open(f_path, "rb") as f:
                response = await client.post(
                    f"{self.base_url}/upload",
                    files={"file": (f_path.name, f)},
                    data={
                        "title": title,
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                    },
                )

                response.raise_for_status()
                return response.json()

    async def upload_batch(
        self,
        file_paths: List[str],
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> List[Dict[str, Any]]:
        """Ingest multiple documents into the RAG system by uploading a batch of files"""
        results = []

        for file_path in file_paths:
            try:
                result = await self.upload_document(
                    file_path=file_path,
                    title=None,
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
            except Exception as e:
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
        top_k: int = 5,
        probes: int = 10,
        max_distance: float = 1.0,
    ):
        """Search for relevant documents in the RAG system based on a query"""
        payload = {
            "query": query,
            "top_k": top_k,
            "probes": probes,
            "max_distance": max_distance,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/search",
                json=payload,
            )

            response.raise_for_status()
            return response.json()
