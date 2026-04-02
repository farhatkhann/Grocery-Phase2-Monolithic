import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
import matplotlib.pyplot as plt

print("[Phase 3.2] Semantic Clustering STARTED", flush=True)

# ======================================================
# PATHS
# ======================================================
# ROOT = Path(_file_).resolve().parents[2]
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "datasets" / "llm_annotations" / "llm_semantic_annotations.json"
OUTPUT_DIR = ROOT / "datasets" / "clusters"
PLOT_DIR = ROOT / "datasets" / "plots"

OUTPUT_FILE = OUTPUT_DIR / "llm_service_clusters.json"

print("Input: ", INPUT_FILE)
print("Output: ", OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)



# ======================================================
# LOAD PHASE 3.1 OUTPUT
# ======================================================
with open(INPUT_FILE, encoding="utf-8") as f:
    annotations = json.load(f)

print(f"Loaded {len(annotations)} functions")

# ======================================================
# SHARED BUSINESS VOCABULARY
# ======================================================
texts = []
for a in annotations:
    texts.append(
        f"{a['intent']} {a['domain_entity']} {a['business_role']}"
    )

# ======================================================
# FUNCTION EMBEDDINGS (Sentence-BERT)
# ======================================================
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)

# ======================================================
# CLUSTERING (HIERARCHICAL – HDBSCAN)
# ======================================================
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=5,
    metric="euclidean"
)

labels = clusterer.fit_predict(embeddings)

# ======================================================
# ASSIGN CLUSTER IDs & SERVICE LABELS
# ======================================================
results = []

for label, item in zip(labels, annotations):
    domain = item["domain_entity"]

    if label == -1:
        service = "UnassignedService"
        role = "Unassigned"
    else:
        service = f"{domain}Service"
        role = item["business_role"]

    function_name = (
    item.get("function_fqn")
    or item.get("function")
    or item.get("name")
)

    if function_name is None:
        continue  

    results.append({
        "function": function_name,
        "cluster_id": service,
        "business_role": role
    })

# ======================================================
# SAVE OUTPUT
# ======================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Clusters written to:", OUTPUT_FILE)

# ======================================================
# OPTIONAL: UMAP VISUALIZATION
# ======================================================
reducer = umap.UMAP(n_components=2, random_state=42)
points = reducer.fit_transform(embeddings)

plt.figure(figsize=(8, 6))
plt.scatter(points[:, 0], points[:, 1], c=labels, cmap="tab10", s=10)
plt.title("UMAP – Semantic Service Clusters")
plt.xlabel("UMAP-1")
plt.ylabel("UMAP-2")
plt.tight_layout()
plt.savefig(PLOT_DIR / "umap_clusters.png")
plt.close()

print("UMAP plot saved (optional)")
print("[Phase 3.2] COMPLETED SUCCESSFULLY")