/**
 * Builds docs/diagrams/sase-section4-t3-t4.mmd and docs/images/sase-section4-t3-t4.png
 * from the Tier 3 / Tier 4 subgraphs and internal edges in sase-networking-flowchart.html.
 *
 * Run from repo root after editing the main flowchart Mermaid:
 *   node scripts/export-sase-section4-diagram.cjs
 *
 * Requires: npx @mermaid-js/mermaid-cli (downloads on first use)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const root = path.join(__dirname, '..');
const htmlPath = path.join(root, 'sase-networking-flowchart.html');
const outMmd = path.join(root, 'docs', 'diagrams', 'sase-section4-t3-t4.mmd');
const outPng = path.join(root, 'docs', 'images', 'sase-section4-t3-t4.png');

function extractPreMermaid(html) {
  const m = html.match(/<pre class="mermaid">([\s\S]*?)<\/pre>/);
  if (!m) throw new Error('No <pre class="mermaid"> block in sase-networking-flowchart.html');
  return m[1].trim();
}

function stripMermaidInit(mmd) {
  return mmd.replace(/^%%\{init:[\s\S]*?%%\s*\n?/m, '');
}

function extractSubgraph(mmd, tierId) {
  const needle = `subgraph ${tierId}[`;
  const start = mmd.indexOf(needle);
  if (start === -1) throw new Error(`Missing ${needle} in flowchart Mermaid`);
  const rest = mmd.slice(start);
  const lines = rest.split('\n');
  let depth = 0;
  const out = [];
  for (const line of lines) {
    if (/^\s*subgraph\s/.test(line)) depth += 1;
    out.push(line);
    if (/^\s*end\s*$/.test(line)) {
      depth -= 1;
      if (depth === 0) break;
    }
  }
  if (depth !== 0) throw new Error(`Unbalanced subgraph for ${tierId}`);
  return out.join('\n');
}

function nodeIdsInSubgraph(subgraphBlock) {
  const ids = new Set();
  for (const line of subgraphBlock.split('\n')) {
    const m = /^\s{4,}(\w+)\["/.exec(line);
    if (m) ids.add(m[1]);
  }
  return ids;
}

function parseEdge(line) {
  const labeled =
    /^\s+(\w+)\s+(-->|-\.->)\|"([^"]*)"\|\s*(\w+)\s*$/.exec(line);
  if (labeled) {
    return {
      from: labeled[1],
      arrow: labeled[2],
      label: labeled[3],
      to: labeled[4],
    };
  }
  const plain = /^\s+(\w+)\s+(-->|-\.->)\s*(\w+)\s*$/.exec(line);
  if (plain) {
    return { from: plain[1], arrow: plain[2], label: null, to: plain[3] };
  }
  return null;
}

function formatEdge(e) {
  if (e.label != null && e.label !== '') {
    return `    ${e.from} ${e.arrow}|"${e.label}"| ${e.to}`;
  }
  return `    ${e.from} ${e.arrow} ${e.to}`;
}

const html = fs.readFileSync(htmlPath, 'utf8');
let mmd = stripMermaidInit(extractPreMermaid(html));

const t3 = extractSubgraph(mmd, 'T3');
const t4 = extractSubgraph(mmd, 'T4');
const ids = new Set([...nodeIdsInSubgraph(t3), ...nodeIdsInSubgraph(t4)]);

const edges = [];
for (const line of mmd.split('\n')) {
  const e = parseEdge(line);
  if (!e) continue;
  if (ids.has(e.from) && ids.has(e.to)) {
    edges.push(formatEdge(e));
  }
}

const header = `%% Auto-generated from sase-networking-flowchart.html (T3/T4 subgraphs + edges between their nodes). Regenerate: node scripts/export-sase-section4-diagram.cjs\n\n`;
const body = ['flowchart TB', '', t3, '', t4, '', ...edges, ''].join('\n');

fs.mkdirSync(path.dirname(outMmd), { recursive: true });
fs.mkdirSync(path.dirname(outPng), { recursive: true });
fs.writeFileSync(outMmd, header + body, 'utf8');

execSync(
  `npx --yes @mermaid-js/mermaid-cli -i "${outMmd}" -o "${outPng}" -b white`,
  { cwd: root, stdio: 'inherit' },
);

console.log('Wrote', path.relative(root, outMmd));
console.log('Wrote', path.relative(root, outPng));
