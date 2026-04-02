# import json
# import re
# from pathlib import Path
# from tqdm import tqdm

# print("[Phase 3.1] LLM-Inspired Semantic Annotation STARTED", flush=True)

# # =====================================================
# # PATH CONFIG (CHANGE ROOT ONLY IF NEEDED)
# # =====================================================
# # ROOT = Path(_file_).resolve().parents[2]

# # TRAD_ANN_DIR = ROOT / "datasets" / "annotations"
# # CODET5_ANN_DIR = (
# #     ROOT / "semantic-analysis"
# #     / "datasetsCodeT5+"
# #     / "annotations"
# # )

# # OUTPUT_FILE = (
# #     ROOT / "llm_annotations"
# #     / "llm_semantic_annotations.json"
# # )

# from pathlib import Path

# # ROOT = src/
# ROOT = Path(__file__).resolve().parent.parent

# # Input: traditional / pre-extracted annotations
# TRAD_ANN_DIR = ROOT / "datasets" / "annotations"

# # Optional: reuse same annotations
# CODET5_ANN_DIR = ROOT / "datasets" / "annotations"

# # Output: LLM semantic annotations
# OUTPUT_FILE = (
#     ROOT
#     / "datasets"
#     / "llm_annotations"
#     / "llm_semantic_annotations.json"
# )

# # print("ROOT:", ROOT)
# # print("Annotations exist:", TRAD_ANN_DIR.exists())
# # print("Output dir:", OUTPUT_FILE.parent)



# # =====================================================
# # UTILITIES
# # =====================================================
# CRUD_KEYWORDS = {
#     "create": "Create",
#     "add": "Create",
#     "save": "Create",
#     "post": "Create",

#     "get": "Read",
#     "find": "Read",
#     "read": "Read",
#     "list": "Read",

#     "update": "Update",
#     "set": "Update",
#     "put": "Update",

#     "delete": "Delete",
#     "remove": "Delete"
# }

# GENERIC_WORDS = {
#     "service", "controller", "application", "impl",
#     "config", "test", "main", "manager"
# }

# def infer_intent(name: str):
#     name = name.lower()
#     for k, v in CRUD_KEYWORDS.items():
#         if k in name:
#             return v
#     return "Process"

# def infer_domain_entity(fqn: str):
#     tokens = re.split(r"[.\$_]", fqn.lower())
#     for t in tokens[::-1]:
#         if t not in GENERIC_WORDS and len(t) > 3:
#             return t.capitalize()
#     return "General"

# def infer_business_role(intent, domain):
#     if intent == "Read":
#         return f"{domain} Query Service"
#     if intent == "Create":
#         return f"{domain} Creation Service"
#     if intent == "Update":
#         return f"{domain} Update Service"
#     if intent == "Delete":
#         return f"{domain} Deletion Service"
#     return f"{domain} Processing Service"

# # =====================================================
# # LOAD FUNCTIONS START FROM JSON FILES
# # =====================================================
# # def load_functions(folder: Path):
# #     functions = set()
# #     for file in folder.glob("*.json"):
# #         with open(file, encoding="utf-8") as f:
# #             data = json.load(f)

# #         # Flat dictionary
# #         if isinstance(data, dict):
# #             for k in data.keys():
# #                 if "." in k:
# #                     functions.add(k)

# #         # Nested structure (modules/functions)
# #         if isinstance(data, dict) and "modules" in data:
# #             for _, module in data["modules"].items():
# #                 for fn in module.get("functions", {}).keys():
# #                     functions.add(fn)

# #     return functions
# def load_functions(folder: Path):
#     functions = set()

#     for file in folder.glob("*.json"):
#         with open(file, encoding="utf-8") as f:
#             data = json.load(f)

#         # Case 1: List of objects
#         if isinstance(data, list):
#             for item in data:
#                 if isinstance(item, dict):
#                     for key in ["function", "function_fqn", "name"]:
#                         if key in item and isinstance(item[key], str):
#                             functions.add(item[key])

#         # Case 2: Flat dict
#         elif isinstance(data, dict):
#             for k, v in data.items():
#                 if isinstance(k, str) and "." in k:
#                     functions.add(k)

#             # Case 3: Nested modules/functions
#             if "modules" in data:
#                 for module in data["modules"].values():
#                     for fn in module.get("functions", {}).keys():
#                         functions.add(fn)

#     return functions

# # =====================================================
# # LOAD FUNCTIONS END FROM JSON FILES
# # =====================================================

# print("Loading Traditional annotations...")
# trad_funcs = load_functions(TRAD_ANN_DIR)

# print("Loading CodeT5+ annotations...")
# codet5_funcs = load_functions(CODET5_ANN_DIR)

# ALL_FUNCTIONS = sorted(trad_funcs.union(codet5_funcs))
# print(f"Total unique functions: {len(ALL_FUNCTIONS)}")

# # =====================================================
# # SEMANTIC ANNOTATION
# # =====================================================
# results = []

# for fqn in tqdm(ALL_FUNCTIONS, desc="Annotating"):
#     intent = infer_intent(fqn)
#     domain = infer_domain_entity(fqn)
#     role = infer_business_role(intent, domain)

#     results.append({
#         "function_fqn": fqn,
#         "intent": intent,
#         "domain_entity": domain,
#         "business_role": role
#     })

# # =====================================================
# # SAVE OUTPUT
# # =====================================================
# OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(results, f, indent=2)

# print("[Phase 3.1] COMPLETED")
# print("Output written to:", OUTPUT_FILE)


#New Code
import json
import re
from pathlib import Path
from tqdm import tqdm

print("[Phase 3.1] LLM-Inspired Semantic Annotation STARTED", flush=True)

# =====================================================
# PATH CONFIG
# =====================================================
ROOT = Path(__file__).resolve().parent.parent  # src/

TRAD_ANN_DIR = ROOT / "datasets" / "annotations"
CODET5_ANN_DIR = ROOT / "datasets" / "annotations"

API_FILE = ROOT / "datasets" / "api_extraction" / "api_endpoints.json"

OUTPUT_FILE = (
    ROOT
    / "datasets"
    / "llm_annotations"
    / "llm_semantic_annotations.json"
)

# =====================================================
# UTILITIES
# =====================================================
CRUD_KEYWORDS = {
    "create": "Create",
    "add": "Create",
    "save": "Create",
    "post": "Create",

    "get": "Read",
    "find": "Read",
    "read": "Read",
    "list": "Read",

    "update": "Update",
    "set": "Update",
    "put": "Update",

    "delete": "Delete",
    "remove": "Delete"
}

GENERIC_WORDS = {
    "service", "controller", "application", "impl",
    "config", "test", "main", "manager"
}

HTTP_TO_INTENT = {
    "POST": "Create",
    "GET": "Read",
    "PUT": "Update",
    "PATCH": "Update",
    "DELETE": "Delete"
}

def infer_intent(text: str):
    text = text.lower()
    for k, v in CRUD_KEYWORDS.items():
        if k in text:
            return v
    return "Process"

def infer_domain_entity(text: str):
    tokens = re.split(r"[\/\.\$_\-]", text.lower())
    for t in reversed(tokens):
        if t not in GENERIC_WORDS and len(t) > 3:
            return t.capitalize()
    return "General"

def infer_business_role(intent, domain):
    if intent == "Read":
        return f"{domain} Query Service"
    if intent == "Create":
        return f"{domain} Creation Service"
    if intent == "Update":
        return f"{domain} Update Service"
    if intent == "Delete":
        return f"{domain} Deletion Service"
    return f"{domain} Processing Service"

# =====================================================
# LOAD FUNCTIONS
# =====================================================
def load_functions(folder: Path):
    functions = set()

    for file in folder.glob("*.json"):
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key in ["function", "function_fqn", "name"]:
                        if key in item:
                            functions.add(item[key])

        elif isinstance(data, dict):
            for k in data.keys():
                if isinstance(k, str) and "." in k:
                    functions.add(k)

            if "modules" in data:
                for module in data["modules"].values():
                    for fn in module.get("functions", {}):
                        functions.add(fn)

    return functions

# =====================================================
# LOAD API ENDPOINTS
# =====================================================
def load_api_endpoints(api_file: Path):
    if not api_file.exists():
        print("⚠ API file not found, skipping API annotation")
        return []

    with open(api_file, encoding="utf-8") as f:
        return json.load(f)

# =====================================================
# FUNCTION SEMANTIC ANNOTATION
# =====================================================
print("Loading function annotations...")
trad_funcs = load_functions(TRAD_ANN_DIR)
codet5_funcs = load_functions(CODET5_ANN_DIR)

ALL_FUNCTIONS = sorted(trad_funcs.union(codet5_funcs))
print(f"Total unique functions: {len(ALL_FUNCTIONS)}")

results = []

for fqn in tqdm(ALL_FUNCTIONS, desc="Annotating Functions"):
    intent = infer_intent(fqn)
    domain = infer_domain_entity(fqn)
    role = infer_business_role(intent, domain)

    results.append({
        "type": "function",
        "function_fqn": fqn,
        "intent": intent,
        "domain_entity": domain,
        "business_role": role
    })

# =====================================================
# API SEMANTIC ANNOTATION
# =====================================================
print("Loading API endpoints...")
api_endpoints = load_api_endpoints(API_FILE)

for api in tqdm(api_endpoints, desc="Annotating APIs"):
    method = api.get("method", "").upper()
    endpoint = api.get("endpoint", "")

    intent = HTTP_TO_INTENT.get(method, infer_intent(endpoint))
    domain = infer_domain_entity(endpoint)
    role = infer_business_role(intent, domain)

    results.append({
        "type": "api",
        "api_endpoint": endpoint,
        "http_method": method,
        "intent": intent,
        "domain_entity": domain,
        "business_role": role,
        "source_file": api.get("source_file")
    })

# =====================================================
# SAVE OUTPUT
# =====================================================
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("[Phase 3.1] COMPLETED SUCCESSFULLY")
print("Output written to:", OUTPUT_FILE)
