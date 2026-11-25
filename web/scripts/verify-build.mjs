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
const denied = /(?:patient_id|patientid|study_\d_(?:analysis_data|fulldata)|(?:ghp_|github_pat_|sk-proj-)[\w-]{15,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)/i;
const hashes = {};
async function scan(dir) {
  for (const entry of await readdir(dir, {withFileTypes:true})) {
    const path = join(dir, entry.name);
    const name = relative(root, path).replaceAll('\\', '/');
    if (entry.isDirectory() && name === 'assets') { await scan(path); continue; }
    if (!entry.isFile() || !(fixed.has(name) || assets.test(name))) throw new Error('Unexpected build file ' + name);
    const body = await readFile(path, 'utf8');
    if (denied.test(body) || /sourceMappingURL/i.test(body)) throw new Error('Forbidden build content in ' + name);
    for (const [, host] of body.matchAll(/https?:\/\/([a-z\d.-]+)/gi)) {
      if (!knownRemote.has(host)) throw new Error('Unexpected endpoint ' + host + ' in ' + name);
    }
    if (name === '_headers' && !body.includes("connect-src 'none'")) throw new Error('CSP is missing its network boundary.');
    hashes[name] = createHash('sha256').update(body).digest('hex');
  }
}
if (!(await lstat(root)).isDirectory()) throw new Error('Build root must be a real directory.');
await scan(root);
if (![...fixed].every(name => hashes[name]) || Object.keys(hashes).length !== 5) throw new Error('Incomplete build.');
console.log(JSON.stringify(hashes, null, 2));
