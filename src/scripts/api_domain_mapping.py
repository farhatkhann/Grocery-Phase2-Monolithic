import json
import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("[Phase 3.3] API–Domain Function Mapping STARTED", flush=True)

# ======================================================
# PATH CONFIG (CORRECT FOR YOUR PROJECT)
# ======================================================
# File is in: src/scripts/api_domain_mapping.py
# Project root is: src/

ROOT = Path(__file__).resolve().parent.parent  # src/
SRC_DIR = ROOT                                # Node.js source lives in src/

ANN_FILE = ROOT / "datasets" / "llm_annotations" / "llm_semantic_annotations.json"
CLUSTER_FILE = ROOT / "datasets" / "clusters" / "llm_service_clusters.json"

OUTPUT_DIR = ROOT / "datasets" / "api_mapping"
OUTPUT_FILE = OUTPUT_DIR / "api_service_mapping.json"
REPORT_FILE = OUTPUT_DIR / "matching_report.json"
RAW_API_FILE = OUTPUT_DIR / "api_endpoints.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("ROOT:", ROOT)
print("Scanning Node.js files in:", SRC_DIR)

# ======================================================
# LOAD DATA
# ======================================================
with open(ANN_FILE, encoding="utf-8") as f:
    annotations = json.load(f)

with open(CLUSTER_FILE, encoding="utf-8") as f:
    clusters = json.load(f)

if not annotations:
    raise RuntimeError("❌ llm_semantic_annotations.json is empty")

# Map function → cluster
func_to_cluster = {
    c["function"]: c["cluster_id"]
    for c in clusters
    if "function" in c
}

# ======================================================
# API EXTRACTION (NODE.JS / EXPRESS)
# ======================================================
endpoint_pattern = re.compile(
    r"""
    (?:app|router)\s*\.\s*
    (get|post|put|delete|patch)\s*
    \(\s*['"]([^'"]+)['"]
    """,
    re.IGNORECASE | re.VERBOSE
)

method_map = {
    "get": "GET",
    "post": "POST",
    "put": "PUT",
    "patch": "PATCH",
    "delete": "DELETE"
}

api_endpoints = []

for js_file in SRC_DIR.rglob("*.js"):
    try:
        content = js_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    for match in endpoint_pattern.finditer(content):
        http_method = match.group(1).lower()
        path = match.group(2)

        api_endpoints.append({
            "endpoint": path,
            "method": method_map.get(http_method, "REQUEST"),
            "source_file": js_file.relative_to(ROOT).as_posix()
        })

print(f"Extracted {len(api_endpoints)} API endpoints", flush=True)

# Save raw extracted APIs (VERY IMPORTANT)
with open(RAW_API_FILE, "w", encoding="utf-8") as f:
    json.dump(api_endpoints, f, indent=2)

if not api_endpoints:
    raise RuntimeError(
        "❌ No API endpoints found.\n"
        "Check:\n"
        "1) Express uses app.get / router.get\n"
        "2) JS files are inside src/\n"
        "3) APIs are not dynamically generated"
    )

# ======================================================
# BUILD SEMANTIC TEXT
# ======================================================
endpoint_texts = [
    f"{e['method']} {e['endpoint']}"
    for e in api_endpoints
]

function_texts = [
    f"{a['intent']} {a['domain_entity']} {a['business_role']}"
    for a in annotations
]

# ======================================================
# EMBEDDINGS (Sentence-BERT)
# ======================================================
print("Generating embeddings...", flush=True)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

endpoint_embeddings = model.encode(endpoint_texts, show_progress_bar=True)
function_embeddings = model.encode(function_texts, show_progress_bar=True)

# ======================================================
# SEMANTIC MATCHING
# ======================================================
similarity = cosine_similarity(endpoint_embeddings, function_embeddings)

results = []
report = []

for i, ep in enumerate(api_endpoints):
    best_idx = int(np.argmax(similarity[i]))
    score = float(similarity[i][best_idx])

    matched_function = annotations[best_idx].get("function_fqn", "")
    # matched_function = annotations[best_idx].get("function_fqn")
    business_role = annotations[best_idx]["business_role"]
    # cluster_id = func_to_cluster.get(matched_function, "UnassignedService")

    results.append({
        "endpoint": ep["endpoint"],
        "method": ep["method"],
        "business_role": business_role,
        # "cluster_id": cluster_id,
        "source_file": ep["source_file"]
    })

    report.append({
        "endpoint": f"{ep['method']} {ep['endpoint']}",
        "matched_function": matched_function,
        "similarity_score": round(score, 3),
        # "cluster_id": cluster_id
    })

# ======================================================
# SAVE OUTPUT
# ======================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("[Phase 3.3] COMPLETED SUCCESSFULLY", flush=True)
print("API → Service mapping written to:", OUTPUT_FILE)
print("Detailed similarity report written to:", REPORT_FILE)
print("Raw extracted APIs written to:", RAW_API_FILE)
