import random


class RAGService:

    # TODO: Implement this fake methods as a separate services
    def fake_embedding(self, text: str):
        # This is a placeholder for an actual embedding function
        return [random.random() for _ in range(768)]

    def fake_chunking(self, content: str):
        # This is a placeholder for an actual chunking function
        return [content[i : i + 100] for i in range(0, len(content), 100)]

    async def query(self, question: str):
        return "Not implemented"

    async def ingest(self, title: str, content: str):
        from app.db.repository import Repository

        repo = Repository()

        doc = await repo.create_document(title=title)

        chunks = self.fake_chunking(content)
        for chunk in chunks:
            embedding = self.fake_embedding(chunk)
            await repo.add_chunk(document_id=doc.id, content=chunk, embedding=embedding)

    async def search(self, query: str):
        from app.db.repository import Repository

        repo = Repository()

        query_embedding = self.fake_embedding(query)
        results = await repo.search(query_embedding=query_embedding, top_k=5)
        return results
