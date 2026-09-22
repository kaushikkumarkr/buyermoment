from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
import joblib


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ccb1"


def load_jsonl(path: Path, source: str | None = None) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if source is None or row.get("source_dataset") == source:
                rows.append(row)
    return rows


def text(row: dict[str, Any]) -> str:
    return " ".join(filter(None, [row.get("context_text"), row.get("product_title"), row.get("product_description")]))


def binary_label(row: dict[str, Any]) -> int | None:
    relevance = row.get("relevance")
    if relevance in {"exact", "substitute", "complement"}:
        return 1
    if relevance == "irrelevant":
        return 0
    return None


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def lexical_score(row: dict[str, Any]) -> float:
    query = tokens(row.get("context_text", ""))
    product = tokens(" ".join(filter(None, [row.get("product_title"), row.get("product_description")])) )
    return len(query & product) / max(1, len(query))


def rank_metrics(rows: list[dict[str, Any]], scores: list[float]) -> dict[str, float | int | None]:
    groups: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for row, score in zip(rows, scores):
        label = binary_label(row)
        if label is not None:
            groups[str(row.get("original_query") or row.get("context_text"))].append((score, label))
    ndcgs: list[float] = []
    reciprocal_ranks: list[float] = []
    for values in groups.values():
        ranked = sorted(values, key=lambda item: item[0], reverse=True)
        positives = sum(label for _, label in ranked)
        if not positives:
            continue
        dcg = sum((2**label - 1) / math.log2(index + 2) for index, (_, label) in enumerate(ranked))
        ideal = sorted((label for _, label in ranked), reverse=True)
        idcg = sum((2**label - 1) / math.log2(index + 2) for index, label in enumerate(ideal))
        ndcgs.append(dcg / idcg if idcg else 0.0)
        reciprocal_ranks.append(next((1 / (index + 1) for index, (_, label) in enumerate(ranked) if label), 0.0))
    return {
        "groups": len(ndcgs),
        "ndcg": sum(ndcgs) / len(ndcgs) if ndcgs else None,
        "mrr": sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else None,
    }


def evaluate(rows: list[dict[str, Any]], scores: list[float], threshold: float = 0.5) -> dict[str, Any]:
    labels = [binary_label(row) for row in rows]
    keep = [index for index, label in enumerate(labels) if label is not None]
    y_true = [labels[index] for index in keep]
    y_score = [scores[index] for index in keep]
    y_pred = [int(score >= threshold) for score in y_score]
    selected_rows = [rows[index] for index in keep]
    return {
        "records": len(keep),
        "positive_rate": sum(y_true) / len(y_true) if y_true else None,
        "precision": precision_score(y_true, y_pred, zero_division=0) if y_true else None,
        "recall": recall_score(y_true, y_pred, zero_division=0) if y_true else None,
        "f1": f1_score(y_true, y_pred, zero_division=0) if y_true else None,
        **rank_metrics(selected_rows, y_score),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Train/evaluate a compact ESCI ProductFit baseline.")
    parser.add_argument("--model-out", type=Path, default=ROOT / "models" / "product_fit" / "product_fit_tfidf.joblib")
    parser.add_argument("--metrics-out", type=Path, default=ROOT / "artifacts" / "product_fit_benchmark.json")
    args = parser.parse_args()

    train_all = load_jsonl(DATA / "train" / "real.jsonl", "amazon_esci")
    esci_hidden = load_jsonl(DATA / "hidden_test" / "real.jsonl", "amazon_esci")
    wands_hidden = load_jsonl(DATA / "hidden_test" / "real.jsonl", "wayfair_wands")
    train = [row for row in train_all if binary_label(row) is not None]
    esci_hidden = [row for row in esci_hidden if binary_label(row) is not None]
    wands_hidden = [row for row in wands_hidden if binary_label(row) is not None]

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=150_000, sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=250, class_weight="balanced", random_state=20260922)),
    ])
    model.fit([text(row) for row in train], [binary_label(row) for row in train])
    args.model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_out, compress=3)

    datasets = {}
    for name, rows in (("esci_hidden", esci_hidden), ("wands_ood", wands_hidden)):
        learned_scores = model.predict_proba([text(row) for row in rows])[:, 1].tolist()
        lexical_scores = [lexical_score(row) for row in rows]
        datasets[name] = {
            "learned_tfidf_logistic": evaluate(rows, learned_scores),
            "lexical_overlap": evaluate(rows, lexical_scores, threshold=0.2),
        }
    result = {
        "version": "product-fit-tfidf-v1",
        "training": {
            "dataset": "Amazon ESCI original labels",
            "records": len(train),
            "labels": {label: sum(binary_label(row) == label for row in train) for label in (0, 1)},
            "features": "word TF-IDF unigrams/bigrams over query + product title + description",
            "classifier": "balanced logistic regression",
            "source_split": "CCB-1 train only",
        },
        "datasets": datasets,
        "model_artifact": {"path": str(args.model_out.relative_to(ROOT)), "sha256": sha256(args.model_out)},
        "production_decision": "CANDIDATE_ONLY; not promoted to hybrid_v1 without comparison to legacy ContextFit and safety regression checks",
    }
    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
