import os
import json
from pathlib import Path
import networkx as nx

print("[Graph Extraction] STARTED", flush=True)

# ==============================
# PATH CONFIG
# ==============================
BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"

INPUT = DATASETS_DIR / "annotations" / "semantic-extraction.json"
OUT_DIR = DATASETS_DIR / "graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_GRAPH = OUT_DIR / "semantic.graphml"

if not INPUT.exists():
    raise FileNotFoundError(f"Semantic input file not found: {INPUT}")

# ==============================
# LOAD DATA
# ==============================
with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"[INFO] Loaded {len(data)} semantic entries")

# ==============================
# INIT GRAPH
# ==============================
G = nx.MultiDiGraph(name="SemanticGraph")

# ==============================
# FUNCTION DEPENDENCIES (IMPORTANT)
# ==============================
# 🔥 Define logical function-level dependencies
# (This replaces fallback in Phase 3.4)
FUNCTION_DEPENDENCIES = {
    "POSTShoppingOrder": ["GETShoppingCart", "GetProducts"],
    "GETShoppingCart": ["GetProducts"],
    "GETCustomerWishlist": ["GETShoppingOrders"],
    "GETCustomerShoppingdetails": ["GETShoppingOrders"],
}

# ==============================
# ADD NODES + BASIC EDGES
# ==============================
for entry in data:

    function = entry.get("function") or entry.get("function_name") or "UnknownFunction"
    entity = entry.get("domain_entity", "UnknownEntity")
    role = entry.get("business_role", "UnknownRole")
    intent = entry.get("intent", "Unknown")

    fn_node = f"FUNC::{function}"
    entity_node = f"ENTITY::{entity}"
    role_node = f"ROLE::{role}"

    # --------------------------
    # ADD NODES
    # --------------------------
    G.add_node(
        fn_node,
        node_type="Function",
        name=function,
        intent=intent
    )

    G.add_node(
        entity_node,
        node_type="DomainEntity",
        name=entity
    )

    G.add_node(
        role_node,
        node_type="BusinessRole",
        name=role
    )

    # --------------------------
    # ADD BASIC RELATIONS
    # --------------------------
    G.add_edge(fn_node, entity_node, relation="OPERATES_ON")
    G.add_edge(fn_node, role_node, relation="IMPLEMENTS")

# ==============================
# ADD FUNCTION CALL RELATIONS (CRITICAL)
# ==============================
print("[INFO] Adding function call dependencies...")

for func, deps in FUNCTION_DEPENDENCIES.items():
    for dep in deps:

        src = f"FUNC::{func}"
        dst = f"FUNC::{dep}"

        if src in G.nodes and dst in G.nodes:
            G.add_edge(src, dst, relation="CALLS")
            print(f"[LINK] {func} ---> {dep}")
        else:
            print(f"[WARN] Skipped dependency: {func} -> {dep} (node missing)")

# ==============================
# SAVE GRAPH
# ==============================
nx.write_graphml(G, OUTPUT_GRAPH)

print("\n[SUCCESS] semantic.graphml created")
print(f"[INFO] Nodes: {len(G.nodes())}")
print(f"[INFO] Edges: {len(G.edges())}")
print(f"[INFO] Saved at: {OUTPUT_GRAPH}")