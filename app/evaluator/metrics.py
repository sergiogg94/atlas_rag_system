from sklearn.metrics.pairwise import cosine_similarity
from typing import List

from app.services.embeddings import EmbeddingsService


class RAGMetrics:
    """Calculate multiple metrics for RAG evaluation"""

    def __init__(self):
        self.model = EmbeddingsService()

    ## Retrival metrics

    def precision_at_k(
        slef, retrieved_docs: List[str], relevant_docs: List[str], k: int = 5
    ) -> float:
        """Ratio of relevant documents in the top-k retrieved docs"""
        retrieved_k = set(retrieved_docs[:k])
        relevant = set(relevant_docs)

        if len(retrieved_k) == 0:
            return 0.0

        intersection = retrieved_k.intersection(relevant)
        return len(intersection) / len(retrieved_k)

    def recall_at_k(
        self, retrieved_docs: List[str], relevant_docs: List[str], k: int = 5
    ) -> float:
        """Ratio of relevant documents retrieved in the top-k results"""
        retrieved_k = set(retrieved_docs[:k])
        relevant = set(relevant_docs)

        if len(relevant) == 0:
            return 0.0

        intersection = retrieved_k.intersection(relevant)
        return len(intersection) / len(relevant)

    def hit_at_k(
        self, retrieved_docs: List[str], relevant_docs: List[str], k: int = 5
    ) -> float:
        """Determines if at least one relevant document is in the top-k retrieved docs"""
        retrieved_k = set(retrieved_docs[:k])
        relevant = set(relevant_docs)

        if len(relevant) == 0:
            return 0.0

        intersection = retrieved_k.intersection(relevant)
        return 1.0 if len(intersection) > 0 else 0.0

    def mean_reciprocal_rank(
        self, retrieved_docs: List[str], relevant_docs: List[str]
    ) -> float:
        """Reciprocal of the rank of the first relevant document"""
        relevant = set(relevant_docs)

        for i, doc in enumerate(retrieved_docs, 1):
            if doc in relevant:
                return 1.0 / i

        return 0.0

    def average_precision(
        self, retrieved_docs: List[str], relevant_docs: List[str]
    ) -> float:
        """Average of precision values computed at each position of a relevant document"""
        relevant = set(relevant_docs)
        precisions = []
        num_relevant_found = 0

        for i, doc in enumerate(retrieved_docs, 1):
            if doc in relevant:
                num_relevant_found += 1
                precision_at_i = num_relevant_found / i
                precisions.append(precision_at_i)

        if len(precisions) == 0:
            return 0.0

        return sum(precisions) / len(precisions)

    ## Generation metrics

    def similarity(self, text_1: str, text_2: str) -> float:
        """Cosine similarity between two sentences"""
        # Encode text
        embeddings = self.model.encode([text_1, text_2])

        # Calculate cosine similarity
        similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

        return similarity_score

    def context_precision(
        self, expected_answer: str, retrieved_chunks: List[str]
    ) -> float:
        """Mean of the cosine similarity between the expected answer and the
        content of every chunk retrived
        """
        # Empty retrived chunks case
        if not retrieved_chunks:
            return 0.0

        # Encode text
        answer_emb = self.model.encode([expected_answer])[0]
        # TODO: Get vectors from the database, implement query method in repository
        chunks_embs = self.model.encode(retrieved_chunks)

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
        relevant_docs: list,
        threshold: float = 0.8,
    ) -> dict:
        """Calculates all the metric for a test case"""

        # Isolate documents and chunks
        retrieved_chunks = [s["content"] for s in sources]
        retrieved_docs = [s["document_title"] for s in sources]

        return {
            # Retrival metrics
            "precision@k": self.precision_at_k(retrieved_docs, relevant_docs, k=5),
            "recall@k": self.recall_at_k(retrieved_docs, relevant_docs, k=5),
            "hit@k": self.hit_at_k(retrieved_docs, relevant_docs, k=5),
            "mrr": self.mean_reciprocal_rank(retrieved_docs, relevant_docs),
            "map": self.average_precision(retrieved_docs, relevant_docs),
            # Generation metrics
            "semantic_similarity": self.similarity(generated_answer, expected_answer),
            "answer_relevance": self.similarity(generated_answer, query),
            "context_precision": self.context_precision(
                expected_answer, retrieved_chunks
            ),
            "is_correct": float(
                self.answer_correctness(generated_answer, expected_answer, threshold)
            ),
        }
