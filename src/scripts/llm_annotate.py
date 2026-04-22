import json
import re
from pathlib import Path
from tqdm import tqdm
INCLUDE_APIS = False

print("[Phase 3.1] LLM-Inspired Semantic Annotation STARTED", flush=True)

# =====================================================
# PATH CONFIG
# =====================================================
ROOT = Path(__file__).resolve().parent.parent

TRAD_ANN_DIR = ROOT / "datasets" / "annotations"
CODET5_ANN_DIR = ROOT / "datasets" / "annotations"

API_FILE = ROOT / "datasets" / "api_extraction" / "api_endpoints.json"

OUTPUT_FILE = (
    ROOT / "datasets" / "llm_annotations" / "llm_semantic_annotations.json"
)

# =====================================================
# CONFIG
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

# =====================================================
# UTILITIES (FIXED)
# =====================================================

def split_words(text: str):
    """Split camelCase + snake_case + dots"""
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'[_\-/\.]', ' ', text)
    return text.lower().split()


def clean_function_name(fqn: str):
    """Extract simple function name from FQN"""
    return fqn.split(".")[-1]

def infer_intent(text: str):
    words = split_words(text)

    for w in words:
        if w in CRUD_KEYWORDS:
            return CRUD_KEYWORDS[w]

    if "signin" in text.lower() or "login" in text.lower():
        return "Authenticate"
    if "signup" in text.lower():
        return "Create"

    return "Process"

def split_words(text: str):
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'[_\-/\.]', ' ', text)
    return text.lower().split()

def normalize_entity(entity):
    if entity.endswith("s") and entity.lower() not in ["address"]:
        return entity[:-1]
    return entity

def infer_domain_entity(text: str):
    words = split_words(text)

    REMOVE = set(list(CRUD_KEYWORDS.keys()) + ["id", "by", "all", "selected"])

    filtered = [w for w in words if w not in REMOVE and w not in GENERIC_WORDS]

    if not filtered:
        return "General"

    # ✅ FIX 1: HANDLE AUTH CASE
    if "sign" in filtered or "login" in filtered:
        return "Auth"
    
    if "order" in text.lower():
        return "Order"

    PRIORITY = [
        "order",
        "customer",
        "product",
        "cart",
        "wishlist",
        "category",
        "address",
        "shopping"
    ]

    for p in PRIORITY:
        if p in filtered:
            return p.capitalize()

    return filtered[0].capitalize()

def infer_business_role(intent, domain):
    if domain.lower() == "auth":
        return f"Auth {intent} Service"

    return f"{domain} {intent} Service"


# =====================================================
# LOAD FUNCTIONS (FIXED)
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
                        val = item.get(key)
                        if val:
                            functions.add(val)

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
        print("⚠ API file not found")
        return []

    with open(api_file, encoding="utf-8") as f:
        return json.load(f)
        
def infer_api_domain(endpoint: str, source_file: str = ""):
    lower = endpoint.lower()

    known = ["customer", "product", "order", "cart", "wishlist", "category", "shopping"]

    for k in known:
        if k in lower:
            return k.capitalize()

    # special case "/"
    if endpoint == "/" and "product" in source_file.lower():
        return "Product"

    # remove params
    parts = [p for p in lower.split("/") if p and not p.startswith(":")]

    if parts:
        return parts[0].capitalize()

    return "Common"


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

    simple_name = clean_function_name(fqn)

    # skip noise
    if simple_name.lower() in GENERIC_WORDS:
        continue

    intent = infer_intent(simple_name)
    domain = infer_domain_entity(simple_name)
    domain = normalize_entity(domain)
    role = infer_business_role(intent, domain)

    results.append({
        "type": "function",
        "function_fqn": fqn,
        "function": simple_name,   # 🔥 important for clustering
        "intent": intent,
        "domain_entity": domain,
        "business_role": role
    })


# =====================================================
# API SEMANTIC ANNOTATION (IMPROVED)
# =====================================================
print("Loading API endpoints...")

api_endpoints = load_api_endpoints(API_FILE)

for api in tqdm(api_endpoints, desc="Annotating APIs"):

    method = api.get("method", "").upper()
    endpoint = api.get("endpoint", "")

    intent = HTTP_TO_INTENT.get(method, infer_intent(endpoint))
    domain = infer_api_domain(endpoint, api.get("source_file", ""))
    domain = normalize_entity(domain)  
    role = infer_business_role(intent, domain)

    if INCLUDE_APIS:
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