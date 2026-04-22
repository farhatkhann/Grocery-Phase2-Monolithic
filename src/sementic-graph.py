import json
import networkx as nx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"

INPUT = DATASETS_DIR / "annotations" / "semantic-extraction.json"
OUT_DIR = DATASETS_DIR / "graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT.exists():
    raise FileNotFoundError(f"Semantic input file not found: {INPUT}")

G = nx.MultiDiGraph(name="SemanticGraph")

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    # SAFE extraction with fallbacks
    function = entry.get("function") or entry.get("function_name") or "UnknownFunction"
    entity = entry.get("domain_entity", "UnknownEntity")
    role = entry.get("business_role", "UnknownRole")
    intent = entry.get("intent", "Unknown")

    fn_node = f"FUNC::{function}"
    entity_node = f"ENTITY::{entity}"
    role_node = f"ROLE::{role}"

    # Nodes with semantic tags
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

    # Semantic relations
    G.add_edge(fn_node, entity_node, relation="OPERATES_ON")
    G.add_edge(fn_node, role_node, relation="IMPLEMENTS")

nx.write_graphml(G, OUT_DIR / "semantic.graphml")
print("✅ semantic.graphml created in src/datasets/graphs/")


