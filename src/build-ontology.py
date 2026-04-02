# build_ontology.py
import json
import os
import pathlib
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD, OWL

# Paths
ROOT = pathlib.Path.cwd()
INPUT = ROOT / "datasets" / "annotations" / "semantic-extraction.json"
OUT_TTL = ROOT / "datasets" / "ontologies" /  "ontology.ttl"
OUT_OWL = ROOT / "datasets" / "ontologies" /  "ontology.owl"  # RDF/XML

if not INPUT.exists():
    print("Input file not found:", INPUT)
    raise SystemExit(1)

data = json.load(INPUT.open("r", encoding="utf8"))

g = Graph()

# Namespaces (change base IRI for your project if you like)
BASE = Namespace("http://example.org/monolith#")
g.bind("base", BASE)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

# Classes
Function = BASE.Function
g.add((Function, RDF.type, OWL.Class))
g.add((Function, RDFS.label, Literal("Function")))

# We'll create domain entity classes on the fly from domain_entity values
domain_entities = set()
for entry in data:
    ent = entry.get("domain_entity") or "GenericEntity"
    domain_entities.add(ent)

for ent in sorted(domain_entities):
    ent_uri = BASE[ent]
    g.add((ent_uri, RDF.type, OWL.Class))
    g.add((ent_uri, RDFS.label, Literal(ent)))

# Object property: relatesTo (Function -> DomainEntity)
relatesTo = BASE.relatesTo
g.add((relatesTo, RDF.type, OWL.ObjectProperty))
g.add((relatesTo, RDFS.label, Literal("relatesTo")))
g.add((relatesTo, RDFS.domain, Function))
# domain_range set to generic (we won't restrict range to specific class)
g.add((relatesTo, RDFS.range, OWL.Thing))

# Data properties for Function
props = {
    "businessRole": XSD.string,
    "intent": XSD.string,
    "httpMethod": XSD.string,
    "route": XSD.string,
    "sourceFile": XSD.string
}
for pname, ptype in props.items():
    p_uri = BASE[pname]
    g.add((p_uri, RDF.type, OWL.DatatypeProperty))
    g.add((p_uri, RDFS.domain, Function))
    g.add((p_uri, RDFS.range, ptype))
    g.add((p_uri, RDFS.label, Literal(pname)))

# Create Function individuals and link to domain entities + add data props
def make_safe_name(s: str) -> str:
    # safe identifier for IRI (simple)
    return "".join(c if c.isalnum() else "_" for c in (s or "unnamed"))

for i, entry in enumerate(data):
    fname = entry.get("function") or f"function_{i}"
    fname_safe = make_safe_name(fname)
    indiv_uri = BASE[f"fn_{fname_safe}_{i}"]  # unique
    g.add((indiv_uri, RDF.type, Function))
    g.add((indiv_uri, RDFS.label, Literal(fname)))

    # relatesTo domain entity
    domain = entry.get("domain_entity") or "GenericEntity"
    domain_uri = BASE[domain]
    g.add((indiv_uri, relatesTo, domain_uri))

    # data properties
    for pname in props.keys():
        val = entry.get(pname[0].lower() + pname[1:])  # businessRole -> businessRole key? we use original keys
        # fallback keys: try exact keys present in your semantic-extraction entries
        if pname == "businessRole":
            val = entry.get("business_role") or entry.get("businessRole") or entry.get("businessrole")
        elif pname == "intent":
            val = entry.get("intent")
        elif pname == "httpMethod":
            val = entry.get("http_method") or entry.get("httpMethod")
        elif pname == "route":
            val = entry.get("route")
        elif pname == "sourceFile":
            val = entry.get("source_file") or entry.get("sourceFile")
        if val:
            g.add((indiv_uri, BASE[pname], Literal(str(val), datatype=XSD.string)))

# Save TTL and RDF/XML
g.serialize(destination=str(OUT_TTL), format="turtle")
g.serialize(destination=str(OUT_OWL), format="xml")

print("Ontology written to:")
print(" -", OUT_TTL)
print(" -", OUT_OWL)
