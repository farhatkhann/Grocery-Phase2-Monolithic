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


#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------

# import os
# import json
# from typing import List, Dict
# from tree_sitter import Language, Parser

# # ---------------------------------------------------
# # STEP 1: Load Tree-Sitter Language
# # ---------------------------------------------------

# # Make sure you have built the language library:
# # git clone https://github.com/tree-sitter/tree-sitter-java
# # Language.build_library('build/my-languages.so', ['tree-sitter-java'])

# LANGUAGE_PATH = "build/my-languages.so"
# JAVA_LANGUAGE = Language(LANGUAGE_PATH, "java")

# parser = Parser()
# parser.set_language(JAVA_LANGUAGE)


# # ---------------------------------------------------
# # STEP 2: API Extraction Class
# # ---------------------------------------------------

# class APIExtractor:
#     def __init__(self, project_path: str):
#         self.project_path = project_path
#         self.api_data = []

#     # -----------------------------------------------
#     # Extract all Java files
#     # -----------------------------------------------
#     def get_java_files(self) -> List[str]:
#         java_files = []
#         for root, _, files in os.walk(self.project_path):
#             for file in files:
#                 if file.endswith(".java"):
#                     java_files.append(os.path.join(root, file))
#         return java_files

#     # -----------------------------------------------
#     # Parse Java file and extract APIs
#     # -----------------------------------------------
#     def extract_apis_from_file(self, file_path: str):
#         with open(file_path, "r", encoding="utf-8") as f:
#             source_code = f.read()

#         tree = parser.parse(bytes(source_code, "utf8"))
#         root_node = tree.root_node

#         self._traverse_tree(root_node, source_code, file_path)

#     # -----------------------------------------------
#     # Traverse AST
#     # -----------------------------------------------
#     def _traverse_tree(self, node, source_code: str, file_path: str):
#         for child in node.children:

#             # Look for method declarations
#             if child.type == "method_declaration":
#                 self._process_method(child, source_code, file_path)

#             # Recursive traversal
#             self._traverse_tree(child, source_code, file_path)

#     # -----------------------------------------------
#     # Process Method Declaration
#     # -----------------------------------------------
#     def _process_method(self, node, source_code: str, file_path: str):

#         method_name = None
#         http_method = None
#         endpoint = None

#         for child in node.children:
#             if child.type == "identifier":
#                 method_name = source_code[child.start_byte:child.end_byte]

#         # Check annotations above method
#         parent = node.parent
#         if parent:
#             for sibling in parent.children:
#                 if sibling.type == "marker_annotation" or sibling.type == "annotation":
#                     annotation_text = source_code[sibling.start_byte:sibling.end_byte]

#                     if "@GetMapping" in annotation_text:
#                         http_method = "GET"
#                         endpoint = self._extract_path(annotation_text)

#                     elif "@PostMapping" in annotation_text:
#                         http_method = "POST"
#                         endpoint = self._extract_path(annotation_text)

#                     elif "@PutMapping" in annotation_text:
#                         http_method = "PUT"
#                         endpoint = self._extract_path(annotation_text)

#                     elif "@DeleteMapping" in annotation_text:
#                         http_method = "DELETE"
#                         endpoint = self._extract_path(annotation_text)

#         if http_method:
#             entity = self._infer_entity_from_path(endpoint)

#             api_info = {
#                 "file": file_path,
#                 "method_name": method_name,
#                 "http_method": http_method,
#                 "endpoint": endpoint,
#                 "entity": entity
#             }

#             self.api_data.append(api_info)

#     # -----------------------------------------------
#     # Extract path from annotation
#     # Example: @GetMapping("/users")
#     # -----------------------------------------------
#     def _extract_path(self, annotation_text: str) -> str:
#         if "(" in annotation_text and ")" in annotation_text:
#             return annotation_text.split("(")[1].split(")")[0].replace('"', '').replace("'", '')
#         return ""

#     # -----------------------------------------------
#     # Infer Domain Entity from endpoint
#     # -----------------------------------------------
#     def _infer_entity_from_path(self, endpoint: str) -> str:
#         if not endpoint:
#             return "Unknown"

#         parts = endpoint.strip("/").split("/")
#         if len(parts) > 0:
#             return parts[0].capitalize()

#         return "Unknown"

#     # -----------------------------------------------
#     # Run extraction
#     # -----------------------------------------------
#     def run(self) -> List[Dict]:
#         java_files = self.get_java_files()

#         for file in java_files:
#             self.extract_apis_from_file(file)

#         return self.api_data


# # ---------------------------------------------------
# # STEP 3: Execute Script
# # ---------------------------------------------------

# if __name__ == "__main__":

#     PROJECT_PATH = "path_to_your_monolith_project"

#     extractor = APIExtractor(PROJECT_PATH)
#     api_results = extractor.run()

#     # Save to JSON
#     with open("api_extracted.json", "w", encoding="utf-8") as f:
#         json.dump(api_results, f, indent=4)

#     print("✅ API extraction completed.")
#     print(f"Total APIs Extracted: {len(api_results)}")

