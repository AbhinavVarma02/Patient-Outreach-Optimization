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
        if (width === 1440 && theme === 'light') {
          const copy = await page.evaluate(() => [document.title, document.body.textContent,
            ...Array.from(document.querySelectorAll('[aria-label], [title], [placeholder], meta[name="description"]'),
              element => ['aria-label', 'title', 'placeholder', 'content'].map(name => element.getAttribute(name)).join(' '))].join(' '));
          expect(copy).not.toContain('\u2014');
        }
        if (browserName === 'chromium' && (width === 1440 || width === 390)) {
          const path = 'qa-output/'+(process.env.OUTREACH_LIVE_URL ? 'live-' : '')+route+'-'+width+'-'+theme+'.png';
          const actual = await page.screenshot({path, fullPage:true});
          if (process.env.OUTREACH_UI_REFERENCE === '1') {
            const suffix = width === 390 ? `-mobile-${theme}` : theme === 'dark' ? '-desktop-dark' : '';
            const name = desktopReferences[route] + suffix;
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
  await page.getByRole('link',{name:'Compare channel costs'}).click();
  await page.getByLabel('Budget (USD)',{exact:true}).fill('0');
  await expect(page.getByText('No outreach',{exact:true})).toBeVisible();
  await page.getByLabel('Eligible population').fill('');
  await expect(page.getByRole('status')).toContainText('Check the population');
  await page.getByRole('button',{name:'Reset assumptions'}).click();
  await page.getByRole('link',{name:'Size the pilot'}).click();
  await page.getByLabel('Share of ideal targeting gain (%)').fill('0');
  await expect(page.getByText('No finite sample size')).toBeVisible();
  await page.getByLabel('Color theme').selectOption('dark');
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
  expect(await page.evaluate(() => ({local: Object.keys(localStorage), session: Object.keys(sessionStorage)})))
    .toEqual({local: ['outreach-theme'], session: []});
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

test('empirical evidence keeps village outcomes and equal-capacity results distinct from patient inputs', async ({page}) => {
  await page.setViewportSize({width:390, height:844});
  await page.goto('/#evidence');
  const sensitivity = page.getByRole('table', {name:'Information-hub assignment sensitivity'});
  await expect(sensitivity.getByRole('row', {name:/Primary health center clustering/})).toContainText('-0.07 to 3.86');
  const policy = page.getByRole('table', {name:'Held-out ambassador allocation vs uniform'});
  await expect(policy.getByRole('row', {name:/Learned village benefit score/})).toContainText('-1.33 to 3.59');
  const sierra = page.getByRole('table', {name:'Replicated effects on adult vaccination'});
  await expect(sierra.getByRole('row', {name:/Mobile package vs control, adult-weighted/})).toContainText('26.1');
  await expect(sierra.getByRole('row', {name:/Extra visit within door-to-door/})).toContainText('-4.8 to 2.5');
  const sierraPolicy = page.getByRole('table', {name:'Exploratory village allocation vs uniform'});
  await expect(sierraPolicy.getByRole('row', {name:/Ridge DR-learner/})).toContainText('-42.7 to 46.5');
  for (const table of [sensitivity, policy, sierra, sierraPolicy]) {
    const fits = await table.evaluate(element => element.parentElement!.scrollWidth <= element.parentElement!.clientWidth);
    expect(fits).toBe(true);
  }
  await expect(page.getByRole('link', {name:/Banerjee et al. data/})).toHaveAttribute('href', 'https://zenodo.org/records/11392582');
  await page.getByText('Trial document extraction', {exact:true}).click();
  await expect(page.getByText(/The verified local model matched 2 of 13/)).toBeVisible();
  await page.getByRole('navigation').getByRole('link', {name:'Patient Targeting'}).click();
  await expect(page.getByText('Fictional inputs', {exact:true})).toBeVisible();
});

test('US payer planner uses CMS benchmarks and keeps randomized estimates out of assumptions', async ({page}) => {
  await page.goto('/#planner');
  const payer = page.locator('section').filter({has:page.getByRole('heading', {name:'Medicare Advantage gap planning'})});
  await expect(payer).toContainText('16.67 pp');
  await payer.getByLabel('Quality measure').selectOption('C02');
  await expect(payer).toContainText('73%');
  await expect(payer).toContainText('54.17 pp');
  await payer.getByLabel('Contact limit').fill('100');
  await expect(payer).toContainText('Too few contacts to close the gap');
  await payer.getByLabel('Reachable members still due').fill('5000');
  await expect(payer.getByRole('status')).toContainText('Reachable members');
  await payer.getByRole('button', {name:'Reset gap assumptions'}).click();
  await expect(payer).toContainText('64%');
  await payer.getByRole('link', {name:/US trial evidence/}).click();
  await expect(page.getByRole('table', {name:'CMS quality and member experience'}))
    .toContainText('480');
  await expect(page.getByRole('table', {name:'UCLA influenza vaccination by assigned reminder'}))
    .toContainText('1.00 (0.98 to 1.01)');
  await expect(page.getByText(/22.04 pp/)).toContainText('effect in Medicare Advantage remains unknown');
});
