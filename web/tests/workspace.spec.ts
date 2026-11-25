import {test, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {createHash} from 'node:crypto';
import {readFile} from 'node:fs/promises';

const headings = {overview:'Which outreach strategy is worth testing?',targeting:'Patient Targeting',
  planner:'Outreach Planner',pilot:'Pilot Designer',evidence:'Evidence & Methods'};
const routes = Object.keys(headings) as (keyof typeof headings)[];
const sizes = [[1440,900],[1280,800],[768,1024],[390,844]];
const desktopReferences = {overview:'overview',targeting:'patient-targeting',planner:'outreach-planner',
  pilot:'pilot-designer',evidence:'evidence-and-methods'};
const referenceDigest = (png: Buffer) => createHash('sha256').update(png).digest('hex');

test('all views fit the viewport in both themes without page errors or external requests', async ({page,browserName,baseURL}) => {
  const failures: string[] = [];
  page.on('pageerror', error => failures.push(error.message));
  page.on('console', message => { if (message.type() === 'error') failures.push(message.text()); });
  page.on('requestfailed', request => failures.push(request.url() + ' ' + request.failure()?.errorText));
  page.on('request', request => {
    if (new URL(request.url()).origin !== new URL(baseURL!).origin) failures.push(request.url());
  });
  for (const [width,height] of sizes) {
    await page.setViewportSize({width,height});
    for (const theme of ['light','dark']) {
      for (const route of routes) {
        const response = await page.goto('/#'+route);
        if (response) expect(response.ok()).toBeTruthy();
        await page.getByLabel('Color theme').selectOption(theme);
        await expect(page.locator('h1')).toHaveText(headings[route]);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
        expect(overflow, route+' '+width+' '+theme).toBe(false);
        if (browserName === 'chromium' && ((width === 1440 && theme === 'light')
          || (width === 390 && (route === 'overview' || route === 'pilot')))) {
          const path = 'qa-output/'+(process.env.OUTREACH_LIVE_URL ? 'live-' : '')+route+'-'+width+'-'+theme+'.png';
          const actual = await page.screenshot({path, fullPage:true});
          if (process.env.OUTREACH_UI_REFERENCE === '1') {
            const name = desktopReferences[route] + (width === 390 ? `-mobile-${theme}` : '');
            const reference = new URL(`../../docs/images/${name}.png`, import.meta.url);
            expect.soft(referenceDigest(actual), `Compare ${path} with docs/images/${name}.png`)
              .toBe(referenceDigest(await readFile(reference)));
          }
        }
      }
    }
  }
  expect(failures).toEqual([]);
});

test('guided workflow recomputes targeting, planner and pilot values and persists theme', async ({page,browserName}) => {
  await page.goto('/');
  const skip = page.getByRole('link',{name:'Skip to content'});
  if (browserName === 'webkit') await skip.focus();
  else await page.keyboard.press('Tab');
  await expect(skip).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('main')).toBeFocused();
  await page.getByRole('link',{name:'Explore targeting'}).click();
  await expect(page.getByRole('cell',{name:'8.2',exact:true})).toBeVisible();
  await page.getByLabel('Effect pattern').selectOption('flat');
  await expect(page.getByRole('cell',{name:'5.4',exact:true})).toHaveCount(3);
  await page.getByRole('link',{name:'Next: compare channel costs'}).click();
  await page.getByLabel('Budget (USD)',{exact:true}).fill('0');
  await expect(page.getByText('No outreach',{exact:true})).toBeVisible();
  await page.getByLabel('Eligible population').fill('');
  await expect(page.getByRole('status')).toContainText('Enter a valid population');
  await page.getByRole('button',{name:'Reset assumptions'}).click();
  await page.getByRole('link',{name:'Next: size the pilot'}).click();
  await page.getByLabel('Ranking quality (%)').fill('0');
  await expect(page.getByText('No finite N')).toBeVisible();
  await page.getByLabel('Color theme').selectOption('dark');
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
});

test('axe WCAG A/AA checks on all views and both themes', async ({page}) => {
  for (const route of routes) {
    await page.goto('/#'+route);
    for (const theme of ['light','dark']) {
      await page.getByLabel('Color theme').selectOption(theme);
      const results = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']).analyze();
      expect(results.violations.map(({id,nodes}) => ({id,targets:nodes.map(node=>node.target)})),
        route+' '+theme).toEqual([]);
    }
  }
});
