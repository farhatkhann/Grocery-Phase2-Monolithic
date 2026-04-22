import os
import json
from pathlib import Path
from collections import defaultdict
import networkx as nx

print("[Phase 3.4] Enriched Graph-Based Metrics STARTED", flush=True)

# ==============================
# PATH CONFIG
# ==============================
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"

GRAPH_PATH = DATASETS_DIR / "graphs" / "semantic.graphml"
CLUSTER_FILE = DATASETS_DIR / "clusters" / "llm_service_clusters.json"
OUTPUT_FILE = DATASETS_DIR / "metrics" / "service_metrics.json"

# ==============================
# LOAD GRAPH
# ==============================
print("[INFO] Loading enriched graph...")
G = nx.read_graphml(GRAPH_PATH)

print(f"[INFO] Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")

# ==============================
# LOAD CLUSTERS
# ==============================
print("[INFO] Loading clusters...")

with open(CLUSTER_FILE, encoding="utf-8") as f:
    cluster_data = json.load(f)

func_to_service = {}
service_funcs = defaultdict(list)

for item in cluster_data:
    func = item["function"]
    service = item["cluster_id"]

    func_to_service[func] = service
    service_funcs[service].append(func)

services = set(service_funcs.keys())

print(f"[INFO] Total services: {len(services)}")

# ==============================
# BUILD SERVICE GRAPH (CORRECT)
# ==============================
print("[INFO] Building service dependency graph (CALLS only)...")

service_edges = defaultdict(set)

for u, v, data in G.edges(data=True):

    # ✅ ONLY consider CALL relationships
    if data.get("relation") != "CALLS":
        continue

    # ✅ extract function names
    if u.startswith("FUNC::") and v.startswith("FUNC::"):
        f1 = u.replace("FUNC::", "")
        f2 = v.replace("FUNC::", "")

        if f1 in func_to_service and f2 in func_to_service:
            s1 = func_to_service[f1]
            s2 = func_to_service[f2]

            if s1 != s2:
                service_edges[s1].add(s2)

# ==============================
# DEBUG: PRINT SERVICE EDGES
# ==============================
print("\n[DEBUG] Service Dependencies:")
for s, deps in service_edges.items():
    print(f"{s} -> {list(deps)}")

# ==============================
# COMPUTE Ca & Ce
# ==============================
print("[INFO] Computing Ca & Ce...")

Ca = {}
Ce = {}

for s in services:
    Ce[s] = len(service_edges.get(s, []))
    Ca[s] = sum(1 for x in services if s in service_edges.get(x, []))

# ==============================
# COMPUTE INSTABILITY
# ==============================
print("[INFO] Computing Instability...")

instability = {}

for s in services:
    total = Ca[s] + Ce[s]
    instability[s] = Ce[s] / total if total > 0 else 0

# ==============================
# COMPUTE COHESION (BETTER LOGIC)
# ==============================
print("[INFO] Computing Cohesion...")

cohesion = {}

for s in services:
    funcs = service_funcs.get(s, [])
    n = len(funcs)

    if n <= 1:
        cohesion[s] = 1.0
    else:
        cohesion[s] = min(1.0, n / 5)

# ==============================
# SAVE OUTPUT
# ==============================
print("[INFO] Saving results...")

os.makedirs(OUTPUT_FILE.parent, exist_ok=True)

result = {}

for s in services:
    result[s] = {
        "Ca": Ca[s],
        "Ce": Ce[s],
        "Instability": round(instability[s], 3),
        "Cohesion": round(cohesion[s], 3),
        "Depends_On": list(service_edges.get(s, []))
    }

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("\n[SUCCESS] Phase 3.4 Completed")
print("Saved at:", OUTPUT_FILE)

# ==============================
# FINAL PRINT
# ==============================
print("\n🔗 FINAL SERVICE DEPENDENCIES:\n")

for s in service_edges:
    for target in service_edges[s]:
        print(f"{s}  --->  {target}")