import json
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_distances

print("[Phase 3.2] Semantic Clustering STARTED", flush=True)

# ======================================================
# PATHS
# ======================================================
ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "datasets" / "llm_annotations" / "llm_semantic_annotations.json"
OUTPUT_DIR = ROOT / "datasets" / "clusters"
PLOT_DIR = ROOT / "datasets" / "plots"

OUTPUT_FILE = OUTPUT_DIR / "llm_service_clusters.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

print("Input:", INPUT_FILE)
print("Output:", OUTPUT_FILE)

# ======================================================
# LOAD DATA
# ======================================================
with open(INPUT_FILE, encoding="utf-8") as f:
    annotations = json.load(f)

print(f"[INFO] Loaded {len(annotations)} annotations")

# ======================================================
# DOMAIN NORMALIZATION (IMPORTANT)
# ======================================================
DOMAIN_MAP = {
    "products": "Product",
    "product": "Product",
    "category": "Product",
    "description": "Product",
    "user": "Auth",
    "auth": "Auth",
    "login": "Auth",
    "signup": "Auth"
}

# ======================================================
# BUILD TEXT FOR EMBEDDING
# ======================================================
texts = []
valid_annotations = []

for a in annotations:
    function_name = (
        a.get("function")
        or a.get("function_fqn", "").split(".")[-1]
        or a.get("name")
        or ""
    )

    if not function_name or function_name.lower() == "unknownfunction":
        continue  # 🔥 remove noise

    intent = a.get("intent", "")
    domain = a.get("domain_entity", "")
    role = a.get("business_role", "")

    # Normalize domain
    domain = DOMAIN_MAP.get(domain.lower(), domain)

    # 🔥 DOMAIN BOOSTING (ADD THIS)
    text = f"{function_name} {domain} {domain} {intent} {domain} {role}".lower()

    texts.append(text)
    a["domain_entity"] = domain  # update normalized
    valid_annotations.append(a)

print(f"[INFO] Valid entries used for clustering: {len(texts)}")

# ======================================================
# EMBEDDINGS
# ======================================================
print("[INFO] Generating embeddings...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

embeddings = model.encode(texts, show_progress_bar=True).astype("float64")

# ======================================================
# DISTANCE MATRIX (FIXED)
# ======================================================
print("[INFO] Computing cosine distance matrix...")
distance_matrix = cosine_distances(embeddings).astype("float64")

# ======================================================
# CLUSTERING
# ======================================================
print("[INFO] Running HDBSCAN clustering...")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=2,
    min_samples=1,
    metric='precomputed'
)

labels = clusterer.fit_predict(distance_matrix)

print("[INFO] Cluster distribution:", Counter(labels))

# ======================================================
# AUTO-NAME CLUSTERS (IMPORTANT)
# ======================================================
cluster_domains = defaultdict(list)

for label, item in zip(labels, valid_annotations):
    if label == -1:
        continue
    cluster_domains[label].append(item["domain_entity"])

cluster_names = {}

for label, domains in cluster_domains.items():
    most_common = Counter(domains).most_common(1)[0][0]
    cluster_names[label] = f"{most_common}Service"

print("[INFO] Cluster Names:", cluster_names)

# ======================================================
# ASSIGN FINAL RESULTS
# ======================================================
results = []

for label, item in zip(labels, valid_annotations):

    function_name = (
        item.get("function")
        or item.get("function_fqn", "").split(".")[-1]
        or item.get("name")
    )

    if label == -1:
        # 🔥 FALLBACK USING DOMAIN
        domain = item.get("domain_entity", "General")

        if domain == "Cart":
            service = "CartService"
        elif domain == "Customer":
            service = "CustomerService"
        elif domain == "Product":
            service = "ProductService"
        elif domain == "Wishlist":
            service = "WishlistService"
        elif domain == "Order":
            service = "OrderService"
        elif domain == "Auth":
            service = "AuthService"
        else:
            service = "UnassignedService"

        role = item.get("business_role", "Unknown")
    else:
        service = cluster_names.get(label, f"Service_{label}")
        role = item.get("business_role", "Unknown")

        if "Order" in role:
            service = "OrderService"

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

print("\n[SUCCESS] Clusters written to:", OUTPUT_FILE)

# ======================================================
# CLUSTER SUMMARY (DEBUG)
# ======================================================
print("\n📊 Cluster Summary:")
summary = Counter([r["cluster_id"] for r in results])
for k, v in summary.items():
    print(f"{k}: {v} functions")

# ======================================================
# UMAP VISUALIZATION
# ======================================================
print("\n[INFO] Generating UMAP visualization...")

reducer = umap.UMAP(n_components=2, random_state=42)
points = reducer.fit_transform(embeddings)

plt.figure(figsize=(8, 6))
plt.scatter(points[:, 0], points[:, 1], c=labels, s=30)
plt.title("UMAP – Semantic Service Clusters")
plt.xlabel("UMAP-1")
plt.ylabel("UMAP-2")
plt.tight_layout()

plot_path = PLOT_DIR / "umap_clusters.png"
plt.savefig(plot_path)
plt.close()

print("[SUCCESS] UMAP plot saved at:", plot_path)

print("\n[Phase 3.2] COMPLETED SUCCESSFULLY")