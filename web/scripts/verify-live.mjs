import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const base = new URL(process.env.OUTREACH_LIVE_URL || 'https://patient-outreach-optimization.pages.dev');
if (base.protocol !== 'https:') throw new Error('Use an HTTPS production URL.');
const ledger = JSON.parse(await readFile(new URL('../../research/reports/public_build_sha256.json', import.meta.url), 'utf8'));
delete ledger._headers;
const expected = new Map(Object.entries(ledger).map(([name, hash]) => [name === 'index.html' ? '/' : '/' + name, hash]));
const browser = await chromium.launch();
try {
  const context = await browser.newContext();
  const page = await context.newPage();
  const received = new Map();
  page.on('response', response => {
    const url = new URL(response.url());
    if (url.origin === base.origin && expected.has(url.pathname)) received.set(url.pathname, response);
  });
  await page.goto(base.href, {waitUntil:'load'});
  await page.locator('h1').waitFor();
  const iconPage = await context.newPage();
  const icon = await iconPage.goto(new URL('/favicon.svg', base).href, {waitUntil:'load'});
  if (icon) received.set('/favicon.svg', icon);
  for (const [path, hash] of expected) {
    const response = received.get(path);
    const headers = response?.headers() || {};
    if (!response?.ok() || createHash('sha256').update(await response.body()).digest('hex') !== hash
        || headers['x-content-type-options'] !== 'nosniff'
        || !headers['content-security-policy']?.includes("connect-src 'none'")
        || !headers['strict-transport-security']) {
      throw new Error('Failed production integrity check for ' + path);
    }
    console.log(path + ' verified over HTTPS');
  }
} finally {
  await browser.close();
}
