// import fs from "fs";
// import path from "path";
// import { fileURLToPath } from "url";

// // Fix __dirname in ES Modules
// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

// // Input & Output
// const INPUT_FILE = path.join(__dirname, "datasets/annotations/api-sementics.json");
// const OUTPUT_FILE = path.join(__dirname, "datasets/annotations/semantic-extraction.json");

// // -------------------------
// // HELPERS
// // -------------------------

// function walkAST(node, cb) {
//     if (!node) return;
//     cb(node);
//     if (node.children) {
//         for (const child of node.children) walkAST(child, cb);
//     }
// }

// function findChild(node, type) {
//     return node.children?.find(c => c.type === type);
// }

// // Extracts "/customer/login"
// function extractStringLiteral(node) {
//     if (!node) return null;
//     if (node.type === "string") {
//         return node.value.replace(/['"]/g, "");
//     }
//     return null;
// }


// function extractHandlerFunction(node) {
//     if (!node) return "UnknownFunction";

//     let found = "UnknownFunction";

//     walkAST(node, child => {
//         // Look ONLY for service.<Method>
//         if (
//             child.type === "member_expression" &&
//             child.children?.[0]?.value === "service"
//         ) {
//             const method = child.children?.[2]?.value;
//             if (method) found = method;
//         }
//     });

//     return found;
// }

// // Extract app.get(), app.post(), router.put(), etc.
// function extractRoutes(astRoot) {
//     const routes = [];

//     walkAST(astRoot, node => {
//         if (node.type !== "call_expression") return;

//         const callee = node.children?.[0];
//         if (!callee || callee.type !== "member_expression") return;

//         const obj = callee.children?.[0]?.value || "";
//         const method = callee.children?.[2]?.value || "";

//         // Only accept app.get/post/put/delete
//         if (obj !== "app" && obj !== "router") return;
//         if (!["get", "post", "put", "delete"].includes(method)) return;

//         const argsNode = findChild(node, "arguments");
//         if (!argsNode) return;

//         // Arguments look like:
//         // "(" string , function ")"
//         const argChildren = argsNode.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");

//         const routeLiteral = argChildren[0];
//         const handlerNode = argChildren[1];

//         const route = extractStringLiteral(routeLiteral) || "/";
//         const handler = extractHandlerFunction(handlerNode);

//         routes.push({
//             method: method.toUpperCase(),
//             route,
//             handler
//         });
//     });

//     return routes;
// }

// // BUSINESS INTENT MAPPING
// const INTENT_MAP = {
//     signup: "Create Account",
//     register: "Create Account",
//     login: "Authenticate User",
//     add: "Create",
//     create: "Create",
//     post: "Create",
//     save: "Create",
//     update: "Update",
//     edit: "Update",
//     put: "Update",
//     remove: "Delete",
//     delete: "Delete",
//     get: "Fetch",
//     read: "Fetch",
//     retrieve: "Fetch",
//     list: "Fetch"
// };

// function detectIntent(name = "") {
//     const n = name.toLowerCase();
//     for (const key of Object.keys(INTENT_MAP)) {
//         if (n.includes(key)) return INTENT_MAP[key];
//     }
//     return "Unknown";
// }

// function guessEntity(route = "") {
//     const known = ["customer", "product", "order", "cart", "wishlist", "address"];
//     const lower = route.toLowerCase();
//     for (const k of known) {
//         if (lower.includes(k)) return k.charAt(0).toUpperCase() + k.slice(1);
//     }
//     return "GenericEntity";
// }

// // ==========================================================
// // MAIN PROCESSOR
// // ==========================================================

// function analyze() {
//     if (!fs.existsSync(INPUT_FILE)) {
//         console.error("api-sementics.json not found");
//         return;
//     }

//     const astFiles = JSON.parse(fs.readFileSync(INPUT_FILE, "utf8"));
//     const summary = [];

//     for (const fileObj of astFiles) {
//         const ast = fileObj.ast;
//         if (!ast) continue;

//         const routes = extractRoutes(ast);

//         routes.forEach(r => {
//             const intent = detectIntent(r.handler);
//             const entity = guessEntity(r.route);

//             summary.push({
//                 function: r.handler,
//                 business_role: intent,
//                 domain_entity: entity,
//                 intent,
//                 http_method: r.method,
//                 route: r.route,
//                 source_file: fileObj.file
//             });
//         });
//     }

//     fs.writeFileSync(OUTPUT_FILE, JSON.stringify(summary, null, 2));
//     console.log("semantic-extraction.json generated successfully.");
// }

// analyze();


//-------------------------------------------------------------------
//-------------------------------------------------------------------

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
// AST HELPERS
// --------------------------------------------------
function walkAST(node, cb) {
    if (!node) return;
    cb(node);
    if (node.children) {
        for (const child of node.children) {
            walkAST(child, cb);
        }
    }
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
        // ES6 imports
        if (node.type === "import_statement") {
            const source = node.children?.find(c => c.type === "string");
            if (source?.value) {
                imports.add(source.value.replace(/['"]/g, ""));
            }
        }

        // CommonJS require()
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
            return (
                current.parent.children?.find(c => c.type === "identifier")?.value ||
                "AnonymousClass"
            );
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

            // service.createUser()
            if (callee?.type === "member_expression") {
                const obj = callee.children?.[0]?.value;
                const method = callee.children?.[2]?.value;
                if (obj && method) calls.add(`${obj}.${method}`);
            }

            // createUser()
            if (callee?.type === "identifier") {
                calls.add(callee.value);
            }
        }
    });

    return [...calls];
}

// --------------------------------------------------
// RETURN TYPE INFERENCE (HEURISTIC)
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
// HANDLER FUNCTION NAME
// --------------------------------------------------
function extractHandlerFunction(node) {
    if (!node) return "UnknownFunction";

    let found = "UnknownFunction";

    walkAST(node, child => {
        if (
            child.type === "member_expression" &&
            child.children?.[0]?.value === "service"
        ) {
            const method = child.children?.[2]?.value;
            if (method) found = method;
        }
    });

    return found;
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

        const obj = callee.children?.[0]?.value || "";
        const method = callee.children?.[2]?.value || "";

        if (!["app", "router"].includes(obj)) return;
        if (!["get", "post", "put", "delete"].includes(method)) return;

        const argsNode = findChild(node, "arguments");
        if (!argsNode) return;

        const args = argsNode.children.filter(
            c => !["(", ")", ","].includes(c.type)
        );

        const routeNode = args[0];
        const handlerNode = args[1];

        routes.push({
            http_method: method.toUpperCase(),
            route: extractStringLiteral(routeNode) || "/",
            handlerNode
        });
    });

    return routes;
}

// --------------------------------------------------
// BUSINESS INTENT & ENTITY
// --------------------------------------------------
const INTENT_MAP = {
    signup: "Create Account",
    register: "Create Account",
    login: "Authenticate User",
    create: "Create",
    add: "Create",
    save: "Create",
    update: "Update",
    edit: "Update",
    put: "Update",
    delete: "Delete",
    remove: "Delete",
    get: "Fetch",
    list: "Fetch",
    retrieve: "Fetch"
};

function detectIntent(name = "") {
    const n = name.toLowerCase();
    for (const k of Object.keys(INTENT_MAP)) {
        if (n.includes(k)) return INTENT_MAP[k];
    }
    return "Unknown";
}

function guessEntity(route = "") {
    const entities = ["customer", "product", "order", "cart", "wishlist", "address"];
    const lower = route.toLowerCase();
    for (const e of entities) {
        if (lower.includes(e)) return e.charAt(0).toUpperCase() + e.slice(1);
    }
    return "GenericEntity";
}

// --------------------------------------------------
// MAIN ANALYSIS
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
            const handlerName = extractHandlerFunction(r.handlerNode);
            const intent = detectIntent(handlerName);

            summary.push({
                function: handlerName,
                class: findEnclosingClass(r.handlerNode),
                signature: extractSignature(r.handlerNode),
                return_type: inferReturnType(r.handlerNode),
                calls: extractCalls(r.handlerNode),
                imports,
                business_role: intent,
                domain_entity: guessEntity(r.route),
                intent,
                http_method: r.http_method,
                route: r.route,
                source_file: fileObj.file
            });
        }
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(summary, null, 2));
    console.log("semantic-extraction.json generated successfully");
}

analyze();







