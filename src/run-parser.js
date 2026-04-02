const fs = require("fs");
const path = require("path");
const Parser = require("tree-sitter");
const JavaScript = require("tree-sitter-javascript");

const projectRoot = process.cwd();

// ---- Convert AST Node into JSON ---- //
function toJSON(node) {
    return {
        type: node.type,
        value: node.text,
        startIndex: node.startIndex,
        endIndex: node.endIndex,
        startPosition: node.startPosition,
        endPosition: node.endPosition,
        children: node.children.map(child => toJSON(child))  // IMPORTANT FIX
    };
}

// ---- Recursively find .js files ---- //
function walk(dir, fileList = []) {
    if (!fs.existsSync(dir)) return fileList;
    const files = fs.readdirSync(dir);
    files.forEach(f => {
        const filePath = path.join(dir, f);
        if (fs.lstatSync(filePath).isDirectory()) {
            walk(filePath, fileList);
        } else if (f.endsWith(".js")) {
            fileList.push(filePath);
        }
    });
    return fileList;
}

async function run() {
    const parser = new Parser();
    parser.setLanguage(JavaScript);

    if (!JavaScript) {
        console.error("❌ Tree-sitter JavaScript language failed to load!");
        process.exit(1);
    }

    const foldersToScan = ["src", "api", "routes", "middleware"];
    let jsFiles = [];

    foldersToScan.forEach(folder => {
        jsFiles.push(...walk(path.join(projectRoot, folder)));
    });

    const results = [];

    for (const file of jsFiles) {
        const code = fs.readFileSync(file, "utf8");
        const tree = parser.parse(code);

        results.push({
            file: path.relative(projectRoot, file),
            ast: toJSON(tree.rootNode)
        });
    }

    const outputDir = path.join(projectRoot, "src/datasets/annotations");
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    console.log("OUTPUT DIRECTORY:", outputDir);
console.log(
    "FULL FILE PATH:",
    path.join(outputDir, "api-sementics.json")
);


    fs.writeFileSync(
        path.join(outputDir, "api-sementics.json"),
        JSON.stringify(results, null, 2)
    );

    console.log("api-sementics.json generated successfully.");
}

run();










