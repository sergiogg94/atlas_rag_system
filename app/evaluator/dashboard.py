import json
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.logging import logger

st.set_page_config(
    page_title="Atlas RAG Evaluator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------
# Custom CSS
# ----------------

st.markdown(
    """
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        color: #333;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
        color: #333;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #17a2b8;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------
# Utility functions
# ----------------


def load_evaluation_results(results_dir: str = "app/evaluator/data/reports"):
    """Load all evaluation reports from the specified directory"""
    results_path = Path(results_dir)
    if not results_path.exists():
        return []

    reports = []
    for file in results_path.glob("evaluation_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["filename"] = file.name
            reports.append(data)

    return sorted(
        reports, key=lambda x: x["experiment_info"]["timestamp"], reverse=True
    )


def format_metric(value: float, metric_type: str = "percentage") -> str:
    """Format metrics for display"""
    if metric_type == "percentage":
        return f"{value*100:.1f}%"
    elif metric_type == "score":
        return f"{value:.3f}"
    elif metric_type == "time":
        return f"{value/1000:.2f}s"
    return f"{value:.2f}"


# ----------------
# Main Content
# ----------------

st.header("Evaluation results")

# Load reports
reports = load_evaluation_results()

# Report selector
report_options = [
    f"{r['experiment_info']['config']["collection_name"]} - "
    f"{r['experiment_info']['timestamp']}"
    for r in reports
]

selected_idx = st.selectbox(
    "Select an evaluation report to view details:",
    range(len(reports)),
    format_func=lambda x: report_options[x],
)

selected_report = reports[selected_idx]

st.markdown("### ⚙️ Experiment Configuration")

config = selected_report["experiment_info"]["config"]
config_df = pd.DataFrame([{"Parameter": k, "Value": v} for k, v in config.items()])
st.table(config_df)

st.session_state.current_report = selected_report

# if 'current_report' in st.session_state:
report = st.session_state.current_report

st.markdown("---")
st.subheader("📊 Evaluation Results")

# Información del experimento
exp_info = report["experiment_info"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Cases", exp_info["total_cases"])
with col2:
    st.metric(
        "Successful", exp_info["successful_cases"], delta=None, delta_color="normal"
    )
with col3:
    st.metric("Failed", exp_info["failed_cases"], delta=None, delta_color="inverse")
with col4:
    success_rate = exp_info["successful_cases"] / exp_info["total_cases"]
    st.metric("Success Rate", format_metric(success_rate))

# Main metrics
st.markdown("### 🎯 Main Metrics")

metrics = report["aggregate_metrics"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Semantic Similarity",
        format_metric(metrics["avg_semantic_similarity"], "score"),
        help="Similarity between generated and expected answer",
    )
with col2:
    st.metric(
        "Accuracy",
        format_metric(metrics["avg_is_correct"]),
        help="Percentage of correct answers",
    )
with col3:
    st.metric(
        "Precision@k",
        format_metric(metrics["avg_precision@k"], "score"),
        help="Precision in top-5 documents",
    )
with col4:
    st.metric(
        "Average Latency",
        format_metric(metrics["avg_latency_ms"], "time"),
        help="Average response time",
    )

# Charts
st.markdown("### 📈 Visual Analysis")

tab1, tab2, tab3 = st.tabs(["By Category", "By Difficulty", "Distribution"])

with tab1:
    # Metrics by category
    cat_data = metrics["by_category"]

    df_cat = pd.DataFrame(
        [
            {
                "Category": cat,
                # "Cases": data["count"],
                "Similarity": data["avg_semantic_similarity"],
                # "Accuracy": data["accuracy"],
            }
            for cat, data in cat_data.items()
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            df_cat,
            x="Category",
            y="Similarity",
            title="Semantic Similarity by Category",
            color="Similarity",
            color_continuous_scale="viridis",
        )
        st.plotly_chart(fig1, use_container_width=True)

    # with col2:
    #     fig2 = px.bar(
    #         df_cat,
    #         x="Category",
    #         y="Accuracy",
    #         title="Accuracy by Category",
    #         color="Accuracy",
    #         color_continuous_scale="rdylgn",
    #     )
    #     st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Analysis by difficulty
    results = report["individual_results"]
    successful = [r for r in results if r["status"] == "success"]

    df_diff = pd.DataFrame(
        [
            {
                "Difficulty": r["difficulty"],
                "Similarity": r["metrics"]["semantic_similarity"],
                "Correct": r["metrics"]["is_correct"],
            }
            for r in successful
        ]
    )

    fig3 = px.box(
        df_diff,
        x="Difficulty",
        y="Similarity",
        title="Similarity Distribution by Difficulty",
        color="Difficulty",
        category_orders={"Difficulty": ["easy", "medium", "hard"]},
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # Metrics distribution
    df_metrics = pd.DataFrame(
        [
            {
                "Test ID": r["test_id"],
                "Similarity": r["metrics"]["semantic_similarity"],
                "Precision@k": r["metrics"]["precision@k"],
                "Recall@k": r["metrics"]["recall@k"],
                "MRR": r["metrics"]["mrr"],
            }
            for r in successful
        ]
    )

    fig4 = go.Figure()

    for metric in ["Similarity", "Precision@k", "Recall@k", "MRR"]:
        fig4.add_trace(go.Histogram(x=df_metrics[metric], name=metric, opacity=0.7))

    fig4.update_layout(
        title="Metrics Distribution",
        barmode="overlay",
        xaxis_title="Score",
        yaxis_title="Frequency",
    )

    st.plotly_chart(fig4, use_container_width=True)

# Individual test cases
st.markdown("### 🔍 Individual Test Cases")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    filter_category = st.multiselect(
        "Filter by category",
        options=sorted(set(r["category"] for r in successful)),
        default=None,
    )

with col2:
    filter_difficulty = st.multiselect(
        "Filter by difficulty", options=["easy", "medium", "hard"], default=None
    )

with col3:
    min_similarity = st.slider("Minimum similarity", 0.0, 1.0, 0.0, 0.1)

# Apply filters
filtered_results = successful

if filter_category:
    filtered_results = [r for r in filtered_results if r["category"] in filter_category]

if filter_difficulty:
    filtered_results = [
        r for r in filtered_results if r["difficulty"] in filter_difficulty
    ]

filtered_results = [
    r for r in filtered_results if r["metrics"]["semantic_similarity"] >= min_similarity
]

st.info(f"📋 Showing {len(filtered_results)} of {len(successful)} cases")

# Display cases
for i, result in enumerate(filtered_results, 1):
    with st.expander(
        f"**{result['test_id']}** | {result['category']} | "
        f"Similarity: {format_metric(result['metrics']['semantic_similarity'], 'score')}"
    ):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Question:**")
            st.info(result["question"])

            st.markdown("**Expected Answer:**")
            st.success(result["expected_answer"])

            st.markdown("**Generated Answer:**")

            # Color based on accuracy
            if result["metrics"]["is_correct"] == 1.0:
                st.markdown(
                    f"<div class='success-box'>{result['generated_answer']}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='error-box'>{result['generated_answer']}</div>",
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown("**Metrics:**")
            metrics_df = pd.DataFrame(
                [
                    {"Metric": k, "Value": format_metric(v, "score")}
                    for k, v in result["metrics"].items()
                ]
            )
            st.dataframe(metrics_df, hide_index=True)

        # # Retrieved chunks
        # st.markdown("**Top 3 Retrieved Chunks:**")
        # for j, chunk in enumerate(result["sources"][:3], 1):
        #     st.text_area(
        #         f"Chunk {j}",
        #         value=chunk[:300] + "..." if len(chunk) > 300 else chunk,
        #         height=100,
        #         disabled=True,
        #     )

# else:
#     st.info("👈 Configure the parameters in the sidebar and press 'Run Evaluation'")

# ----------------
# FOOTER
# ----------------

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    Atlas RAG System Evaluation Dashboard v1.0
</div>
""",
    unsafe_allow_html=True,
)
