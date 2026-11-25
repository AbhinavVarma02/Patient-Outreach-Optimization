import { lstat, readdir, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '../dist');
const fixed = new Set(['index.html', 'favicon.svg', '_headers']);
const assets = /^assets\/index-[\w-]+\.(js|css)$/;
const knownRemote = new Set([
  'www.w3.org', 'www.w3.org.', 'react.dev', 'pubmed.ncbi.nlm.nih.gov',
  'media.springernature.com', 'clinicaltrials.gov', 'osf.io',
]);
const reviewedLinks = new Set([
  'https://zenodo.org/records/11392582',
  'https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/HARYANA_RESEARCH.md',
  'https://doi.org/10.7910/DVN/PRXF5Z',
  'https://doi.org/10.1001/jamanetworkopen.2024.46693',
  'https://www.cms.gov/files/document/2027-star-ratings-technical-notes.pdf',
  'https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/SIERRA_LEONE_RESEARCH.md',
  'https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/blob/main/docs/AI_EVALUATION.md',
]);
const denied = /(?:patient_id|patientid|study_\d_(?:analysis_data|fulldata)|(?:ghp_|github_pat_|sk-proj-)[\w-]{15,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)/i;
const hashes = {};
async function scan(dir) {
  for (const entry of await readdir(dir, {withFileTypes:true})) {
    const path = join(dir, entry.name);
    const name = relative(root, path).replaceAll('\\', '/');
    if (entry.isDirectory() && name === 'assets') { await scan(path); continue; }
    if (!entry.isFile() || !(fixed.has(name) || assets.test(name))) throw new Error('Unexpected build file ' + name);
    const bytes = await readFile(path);
    const body = new TextDecoder('utf-8', {fatal: true}).decode(bytes);
    if (denied.test(body) || /sourceMappingURL/i.test(body)) throw new Error('Forbidden build content in ' + name);
    for (const [url, host] of body.matchAll(/https?:\/\/([a-z\d.-]+)[^\s"'<>),`}]*/gi)) {
      if (!knownRemote.has(host) && !reviewedLinks.has(url)) throw new Error('Unexpected endpoint ' + host + ' in ' + name);
    }
    if (name === '_headers' && !body.includes("connect-src 'none'")) throw new Error('CSP is missing its network boundary.');
    hashes[name] = createHash('sha256').update(bytes).digest('hex');
  }
}
if (!(await lstat(root)).isDirectory()) throw new Error('Build root must be a real directory.');
await scan(root);
const names = Object.keys(hashes);
const javascript = names.filter(name => assets.test(name) && name.endsWith('.js'));
const stylesheets = names.filter(name => assets.test(name) && name.endsWith('.css'));
if (![...fixed].every(name => Object.hasOwn(hashes, name)) || javascript.length !== 1 || stylesheets.length !== 1) {
  throw new Error('Build must contain one JavaScript bundle, one stylesheet and the three fixed files.');
}
const html = await readFile(join(root, 'index.html'), 'utf8');
if (!html.includes(`src="/${javascript[0]}"`) || !html.includes(`href="/${stylesheets[0]}"`)) {
  throw new Error('Index does not reference the approved bundles.');
}
console.log(JSON.stringify(hashes, null, 2));
