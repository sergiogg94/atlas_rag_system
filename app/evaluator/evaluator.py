import json
from pathlib import Path
from typing import Dict, List
from time import perf_counter
from datetime import datetime

from app.core.logging import logger
from app.services.rag_service import RAGService
from app.evaluator.metrics import RAGMetrics


class RAGEvaluator:
    def __init__(
        self,
        collection_name: str = "sprintstep_docs",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 5,
        probes: int = 10,
        max_distance: float = 1.0,
        correctness_threshold: float = 0.8,
    ):
        self.rag_service = RAGService()
        self.metrics = RAGMetrics()

        self.config = {
            # Dataset config
            "collection_name": collection_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            # Search config
            "top_k": top_k,
            "probes": probes,
            "max_distance": max_distance,
            "correctness_threshold": correctness_threshold,
        }

    async def load_test_dataset(self, dataset_path: str) -> Dict:
        """Load the test set from a given path"""
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["test_cases"]

    async def evaluate_test_case(self, test_case: Dict) -> Dict:
        """Evaluates a single test case"""
        logger.info(f"Evaluating case: {test_case["id"]}")
        start_time = perf_counter()

        try:
            # Query the RAG service
            result = await self.rag_service.query(
                question=test_case["question"],
                top_k=self.config["top_k"],
                probes=self.config["probes"],
                max_distance=self.config["max_distance"],
                temperature=0.0,
            )

            # Calculate metrics
            metrics = await self.metrics.calculate_metrics(
                query=test_case["question"],
                generated_answer=result["answer"],
                expected_answer=test_case["expected_answer"],
                sources=result["sources"],
                relevant_docs=test_case["relevant_docs"],
                threshold=self.config["correctness_threshold"],
            )

            latency_ms = round((perf_counter() - start_time) * 1000, 2)
            logger.info("Evaluation completed")

            return {
                "test_id": test_case["id"],
                "category": test_case["category"],
                "difficulty": test_case["difficulty"],
                "query_type": test_case["query_type"],
                "question": test_case["question"],
                "expected_answer": test_case["expected_answer"],
                "generated_answer": result["answer"],
                "sources": result["sources"],
                "metrics": metrics,
                "latency_ms": latency_ms,
                "status": "success",
            }

        except Exception as e:
            latency_ms = round((perf_counter() - start_time) * 1000, 2)
            logger.error("Error during evaluation")

            return {
                "test_id": test_case["id"],
                "category": test_case["category"],
                "question": test_case["question"],
                "status": "error",
                "error_message": str(e),
                "latency_ms": latency_ms,
            }

    async def run_full_evaluation(
        self, dataset_path: str, output_path: str = "app/evaluator/data/reports"
    ):
        """Runs the full evaluation process on a given dataset and saves the report"""
        logger.info("Starting full evaluation")
        # Load dataset
        test_cases = await self.load_test_dataset(dataset_path)

        # Evaluate cases
        results = []
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"Case {i} / {len(test_cases)}")
            result = await self.evaluate_test_case(test_case)
            results.append(result)

        # Calculate aggregate metrics
        aggregates = self._calculate_aggregate_metrics(results)

        # Final report
        report = {
            "experiment_info": {
                "timestamp": datetime.now().isoformat(),
                "config": self.config,
                "total_cases": len(test_cases),
                "successful_cases": sum(1 for r in results if r["status"] == "success"),
                "failed_cases": sum(1 for r in results if r["status"] == "error"),
            },
            "aggregate_metrics": aggregates,
            "individual_results": results,
        }

        # Save report
        report_path = self._save_report(report, output_path)
        logger.info(f"Evaluation completed. Report saved to {report_path}")

        return report

    def _calculate_aggregate_metrics(self, results: List[Dict]):
        """Calculate aggregate metrics across all test cases"""
        successful_results = [r for r in results if r["status"] == "success"]

        if not successful_results:
            return {}

        # General metrics
        aggregates = {}
        all_metrics = [r["metrics"] for r in successful_results]
        aggregates.update(self._aggregate_metrics_list(all_metrics))
        aggregates["avg_latency_ms"] = sum(
            r["latency_ms"] for r in successful_results
        ) / len(successful_results)

        # By category
        categories = set(r["category"] for r in successful_results)
        aggregates["by_category"] = {}

        for cat in categories:
            cat_results = [r for r in successful_results if r["category"] == cat]
            cat_metrics = [r["metrics"] for r in cat_results]
            aggregates["by_category"][cat] = self._aggregate_metrics_list(cat_metrics)

        # By difficulty
        difficulties = set(r["difficulty"] for r in successful_results)
        aggregates["by_difficulty"] = {}

        for diff in difficulties:
            diff_results = [r for r in successful_results if r["difficulty"] == diff]
            diff_metrics = [r["metrics"] for r in diff_results]
            aggregates["by_difficulty"][diff] = self._aggregate_metrics_list(
                diff_metrics
            )

        return aggregates

    def _aggregate_metrics_list(self, metrics: List[Dict]) -> Dict:
        """Calculate average, min, and max for each metric in a list of metric dictionaries"""
        aggregates = {}

        for key in metrics[0].keys():
            values = [r[key] for r in metrics]
            aggregates[f"avg_{key}"] = sum(values) / len(values)
            aggregates[f"min_{key}"] = min(values)
            aggregates[f"max_{key}"] = max(values)

        return aggregates

    def _save_report(self, report: Dict, output_dir: str) -> str:
        """Saves the evaluation report to a JSON file in the specified output directory"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_{timestamp}.json"
        output_path = Path(output_dir) / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return str(output_path)
