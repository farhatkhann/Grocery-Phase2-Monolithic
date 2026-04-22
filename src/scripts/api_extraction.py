import json
import re
from pathlib import Path

print("[API Extraction] STARTED", flush=True)

# ======================================================
# PATH CONFIG
# ======================================================
ROOT = Path(__file__).resolve().parent.parent  # src/

assert ROOT.name == "src", f"ROOT is not src! Got: {ROOT}"

SRC_DIR = ROOT  # Node.js source lives in src/

OUTPUT_DIR = ROOT / "datasets" / "api_extraction"
OUTPUT_FILE = OUTPUT_DIR / "api_endpoints.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("ROOT:", ROOT)
print("Scanning source dir:", SRC_DIR)
print("Output file:", OUTPUT_FILE)

# ======================================================
# EXPRESS API REGEX
# Supports:
# app.get("/path", ...)
# router.post('/path', ...)
# ======================================================
endpoint_pattern = re.compile(
    r"\b(app|router)\.(get|post|put|delete|patch)\s*\(\s*[\"']([^\"']+)[\"']",
    re.IGNORECASE
)

api_endpoints = []

# ======================================================
# SCAN JS FILES
# ======================================================
for js_file in SRC_DIR.rglob("*.js"):
    # Skip node_modules if present
    if "node_modules" in js_file.parts:
        continue

    with open(js_file, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    for match in endpoint_pattern.finditer(content):
        method = match.group(2).upper()
        path = match.group(3)

        api_endpoints.append({
            "endpoint": path,
            "method": method,
            "source_file": js_file.relative_to(ROOT).as_posix()
        })

print(f"Extracted {len(api_endpoints)} API endpoints", flush=True)

# ======================================================
# FAIL FAST IF NOTHING FOUND
# ======================================================
if not api_endpoints:
    raise ValueError(
        "❌ No APIs found.\n"
        "Make sure your Express routes use app.get/post or router.get/post."
    )

# ======================================================
# SAVE OUTPUT
# ======================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(api_endpoints, f, indent=2)

print("[API Extraction] COMPLETED SUCCESSFULLY", flush=True)
print("API list written to:", OUTPUT_FILE)