import {defineConfig} from '@playwright/test';
const liveURL = process.env.OUTREACH_LIVE_URL;
const localURL = 'http://127.0.0.1:43891';
export default defineConfig({
  testDir: './tests', testMatch: '**/*.spec.ts', retries:0, workers:2,
  outputDir: liveURL ? 'qa-output/live-traces' : 'qa-output/traces',
  use: {baseURL: liveURL || localURL, trace:'retain-on-failure'},
  webServer: liveURL ? undefined : {command: 'npm run preview -- --host 127.0.0.1 --port 43891 --strictPort',
    url:localURL, reuseExistingServer: false},
  projects: ['chromium','firefox','webkit'].map(browserName => ({name:browserName, use:{browserName} as const})),
});
