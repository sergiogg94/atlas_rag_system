from sklearn.metrics.pairwise import cosine_similarity
from app.services.embeddings import EmbeddingsService


class RAGMetrics:
    """Calculate multiple metrics for RAG evaluation"""

    def __init__(self):
        self.model = EmbeddingsService()

    def similarity(self, text_1: str, text_2: str) -> float:
        """Cosine similarity between two sentences"""
        # Encode text
        embeddings = self.model.encode([text_1, text_2])

        # Calculate cosine similarity
        similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

        return similarity_score

    def context_precision(self, expected_answer: str, retrieved_chunks: list) -> float:
        """Mean of the cosine similarity between the expected answer and the
        content of every chunk retrived
        """
        # Empty retrived chunks case
        if not retrieved_chunks:
            return 0.0

        # Encode text
        answer_emb = self.model.encode([expected_answer])[0]
        # TODO: Get vectors from the database, implement query method in repository
        chunks_embs = self.model.encode([c["content"] for c in retrieved_chunks])

        # Similarities
        similarities = []
        for chunk_emb in chunks_embs:
            sim = cosine_similarity([answer_emb], [chunk_emb])[0][0]
            similarities.append(sim)

        # Return average similarity as context precision
        return sum(similarities) / len(similarities)

    def answer_correctness(
        self, generated_aswer: str, expected_answer: str, threshold: float = 0.8
    ) -> bool:
        """Decides if the given answer is correct based on the cosine similarity"""
        sim = self.similarity(generated_aswer, expected_answer)

        return sim >= threshold

    def calculate_metrics(
        self,
        query: str,
        generated_answer: str,
        expected_answer: str,
        sources: list,
        threshold: float = 0.8,
    ) -> dict:
        """Calculates all the metric for a test case"""
        return {
            "semantic_similarity": self.similarity(generated_answer, expected_answer),
            "answer_relevance": self.similarity(generated_answer, query),
            "context_precision": self.context_precision(expected_answer, sources),
            "is_correct": float(
                self.answer_correctness(generated_answer, expected_answer, threshold)
            ),
        }
