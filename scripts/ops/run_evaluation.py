import asyncio

from app.core.logging import logger
from app.evaluator.evaluator import RAGEvaluator


async def main():
    evaluator = RAGEvaluator(
        collection_name="sprintstep_mini",
        chunk_size=500,
        chunk_overlap=50,
        top_k=5,
        max_distance=0.98,
        correctness_threshold=0.8,
    )

    report = await evaluator.run_full_evaluation(
        dataset_path="app/evaluator/data/test_dataset_sprintstep_mini.json"
    )

    logger.info(f"Successful cases: {report['experiment_info']['successful_cases']}")
    logger.info(f"Failed cases: {report['experiment_info']['failed_cases']}")
    logger.info(
        f"Average semantic similarity: {report['aggregate_metrics']['avg_semantic_similarity']:.3f}"
    )
    logger.info(f"Accuracy: {report['aggregate_metrics']['avg_is_correct']:.2%}")


if __name__ == "__main__":
    asyncio.run(main())
