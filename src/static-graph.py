
import json
import networkx as nx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"

INPUT = DATASETS_DIR / "annotations" / "api-sementics.json"
OUT_DIR = DATASETS_DIR / "graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

G = nx.DiGraph(name="StaticCodeGraph")

with open(INPUT, "r", encoding="utf-8") as f:
    files = json.load(f)

for fobj in files:
    file_path = fobj["file"]
    package = file_path.replace("\\", "/").split("/")[0]

    pkg_node = f"PKG::{package}"
    file_node = f"FILE::{file_path}"

    G.add_node(pkg_node, node_type="Package")
    G.add_node(file_node, node_type="File")
    G.add_edge(pkg_node, file_node, relation="CONTAINS")

    def walk(node):
        if node["type"] in ["function_declaration", "method_definition"]:
            fn_name = node.get("value", "anonymous")
            fn_node = f"FUNC::{fn_name}"
            G.add_node(fn_node, node_type="Function")
            G.add_edge(file_node, fn_node, relation="HAS_FUNCTION")

        for c in node.get("children", []):
            walk(c)

    walk(fobj["ast"])

nx.write_gml(G, OUT_DIR / "static.gml")
print("✅ static.gml created in src/datasets/graphs/")




