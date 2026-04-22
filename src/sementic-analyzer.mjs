import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// --------------------------------------------------
// FIX __dirname FOR ES MODULES
// --------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// --------------------------------------------------
// INPUT / OUTPUT
// --------------------------------------------------
const INPUT_FILE = path.join(__dirname, "datasets/annotations/api-sementics.json");
const OUTPUT_FILE = path.join(__dirname, "datasets/annotations/semantic-extraction.json");

// --------------------------------------------------
// NORMALIZATION (IMPORTANT)
// --------------------------------------------------
function normalizeText(text = "") {
    return text
        .replace(/shoping/gi, "shopping")   // fix typo
        .replace(/custmer/gi, "customer")
        .replace(/prodct/gi, "product");
}

// --------------------------------------------------
// AST HELPERS
// --------------------------------------------------
function walkAST(node, cb) {
    if (!node) return;
    cb(node);
    node.children?.forEach(child => walkAST(child, cb));
}

function addParentLinks(node, parent = null) {
    node.parent = parent;
    node.children?.forEach(child => addParentLinks(child, node));
}

function findChild(node, type) {
    return node.children?.find(c => c.type === type);
}

function extractStringLiteral(node) {
    if (!node) return null;
    if (node.type === "string") {
        return node.value.replace(/['"]/g, "");
    }
    return null;
}

// --------------------------------------------------
// IMPORT EXTRACTION
// --------------------------------------------------
function extractImports(astRoot) {
    const imports = new Set();

    walkAST(astRoot, node => {
        if (node.type === "import_statement") {
            const source = node.children?.find(c => c.type === "string");
            if (source?.value) {
                imports.add(source.value.replace(/['"]/g, ""));
            }
        }

        if (
            node.type === "call_expression" &&
            node.children?.[0]?.value === "require"
        ) {
            const args = findChild(node, "arguments");
            const literal = args?.children?.find(c => c.type === "string");
            if (literal?.value) {
                imports.add(literal.value.replace(/['"]/g, ""));
            }
        }
    });

    return [...imports];
}

// --------------------------------------------------
// CLASS DETECTION
// --------------------------------------------------
function findEnclosingClass(node) {
    let current = node;
    while (current?.parent) {
        if (current.parent.type === "class_declaration") {
            return current.parent.children?.find(c => c.type === "identifier")?.value || "AnonymousClass";
        }
        current = current.parent;
    }
    return null;
}

// --------------------------------------------------
// FUNCTION SIGNATURE
// --------------------------------------------------
function extractSignature(fnNode) {
    const paramsNode = findChild(fnNode, "formal_parameters");
    if (!paramsNode) return "()";

    const params = paramsNode.children
        .filter(c => c.type === "identifier")
        .map(c => c.value);

    return `(${params.join(", ")})`;
}

// --------------------------------------------------
// FUNCTION CALLS
// --------------------------------------------------
function extractCalls(fnNode) {
    const calls = new Set();

    walkAST(fnNode, node => {
        if (node.type === "call_expression") {
            const callee = node.children?.[0];

            if (callee?.type === "member_expression") {
                const obj = callee.children?.[0]?.value;
                const method = callee.children?.[2]?.value;
                if (obj && method) calls.add(`${obj}.${method}`);
            }

            if (callee?.type === "identifier") {
                calls.add(callee.value);
            }
        }
    });

    return [...calls];
}

// --------------------------------------------------
// RETURN TYPE
// --------------------------------------------------
function inferReturnType(fnNode) {
    let hasReturn = false;
    let hasAwait = false;

    walkAST(fnNode, node => {
        if (node.type === "return_statement") hasReturn = true;
        if (node.type === "await_expression") hasAwait = true;
    });

    if (hasAwait) return "Promise";
    if (hasReturn) return "Response";
    return "void";
}

// --------------------------------------------------
// FUNCTION NAME EXTRACTION
// --------------------------------------------------
function extractHandlerFunction(node) {
    if (!node) return "UnknownFunction";

    if (node.type === "identifier") return node.value;

    if (node.type === "member_expression") {
        const method = node.children?.[2]?.value;
        if (method) return method;
    }

    let found = null;

    walkAST(node, child => {
        if (
            child.type === "member_expression" &&
            child.children?.[0]?.value === "service"
        ) {
            const method = child.children?.[2]?.value;
            if (method && !found) found = method;
        }
    });

    return found || "UnknownFunction";
}

// --------------------------------------------------
// DERIVE FUNCTION NAME
// --------------------------------------------------
function deriveFunctionName(handlerName, route, method) {
    if (handlerName && handlerName !== "UserAuth" && handlerName !== "UnknownFunction") {
        return normalizeText(handlerName);
    }

    let clean = normalizeText(route)
        .replace(/[:]/g, "")
        .replace(/\//g, " ")
        .replace(/[^a-zA-Z0-9 ]/g, "")
        .trim();

    clean = clean
        .split(" ")
        .filter(Boolean)
        .map(w => w.charAt(0).toUpperCase() + w.slice(1))
        .join("");

    return method + clean;
}

// --------------------------------------------------
// INTENT DETECTION
// --------------------------------------------------
function detectIntent(name = "", route = "", method = "") {
    const text = `${name} ${route}`.toLowerCase();

    if (text.includes("login") || text.includes("signin")) return "Authenticate";
    if (text.includes("signup") || text.includes("register")) return "Create";

    if (method === "POST") return "Create";
    if (method === "GET") return "Read";
    if (method === "PUT") return "Update";
    if (method === "DELETE") return "Delete";

    return "Process";
}
// function detectIntent(name = "", route = "", method = "") {
//     if (method === "POST") return "Create";
//     if (method === "GET") return "Read";
//     if (method === "PUT") return "Update";
//     if (method === "DELETE") return "Delete";

//     const text = `${name} ${route}`.toLowerCase();

//     if (text.includes("login")) return "Authenticate";

//     return "Process";
// }

// --------------------------------------------------
// DOMAIN DETECTION
// --------------------------------------------------
function guessEntity(route = "", source_file = "") {
    const lower = route.toLowerCase();

        const known = ["customer", "product", "category", "cart", "wishlist", "order", "shopping"];

    for (const e of known) {
        if (lower.includes(e)) {
            return e.charAt(0).toUpperCase() + e.slice(1);
        }
    }

    // Fix root "/"
    if (route === "/" && source_file.toLowerCase().includes("product")) {
        return "Product";
    }

    // remove dynamic params
    const parts = lower.split("/").filter(p => p && !p.startsWith(":"));

    if (parts.length > 0) {
        return parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
    }

    return "Common";
}

// --------------------------------------------------
// ROUTE EXTRACTION
// --------------------------------------------------
function extractRoutes(astRoot) {
    const routes = [];

    walkAST(astRoot, node => {
        if (node.type !== "call_expression") return;

        const callee = node.children?.[0];
        if (!callee || callee.type !== "member_expression") return;

        const obj = callee.children?.[0]?.value;
        const method = callee.children?.[2]?.value;

        if (!["app", "router"].includes(obj)) return;
        if (!["get", "post", "put", "delete"].includes(method)) return;

        const argsNode = findChild(node, "arguments");
        if (!argsNode) return;

        const args = argsNode.children.filter(
            c => !["(", ")", ","].includes(c.type)
        );

        routes.push({
            http_method: method.toUpperCase(),
            route: extractStringLiteral(args[0]) || "/",
            handlerNode: args[1]
        });
    });

    return routes;
}

// --------------------------------------------------
// MAIN
// --------------------------------------------------
function analyze() {
    if (!fs.existsSync(INPUT_FILE)) {
        console.error("api-sementics.json not found");
        return;
    }

    const astFiles = JSON.parse(fs.readFileSync(INPUT_FILE, "utf8"));
    const summary = [];

    for (const fileObj of astFiles) {
        const ast = fileObj.ast;
        if (!ast) continue;

        addParentLinks(ast);

        const imports = extractImports(ast);
        const routes = extractRoutes(ast);

        for (const r of routes) {
            let handlerName = extractHandlerFunction(r.handlerNode);
            handlerName = deriveFunctionName(handlerName, r.route, r.http_method);

            const intent = detectIntent(handlerName, r.route, r.http_method);
            const domain = guessEntity(r.route, fileObj.file);

            summary.push({
                function: handlerName,
                class: findEnclosingClass(r.handlerNode),
                signature: extractSignature(r.handlerNode),
                return_type: inferReturnType(r.handlerNode),
                calls: extractCalls(r.handlerNode),
                imports,
                business_role: intent,
                domain_entity: domain,
                intent,
                http_method: r.http_method,
                route: r.route,
                source_file: fileObj.file
            });
        }
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(summary, null, 2));
    console.log("✅ semantic-extraction.json generated successfully");
}

analyze();







