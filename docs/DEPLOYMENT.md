# Deployment

Deploy only a build that passed the publication check and browser test matrix. Pages Direct Upload serves web/dist with the bundled security headers. Current intended project slug is patient-outreach-optimization. Wrangler 4.168.0 was selected from the official npm package. Disable telemetry during release if required by the operator.

```sh
npm exec --yes --package=wrangler@4.168.0 -- wrangler whoami
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages project list
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages project create patient-outreach-optimization --production-branch main
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages deploy web/dist --project-name patient-outreach-optimization --branch main
```

Run creation only when the verified account lacks that project. Confirm production domain and HTTPS response headers. Set OUTREACH_LIVE_URL to the verified URL and rerun the browser suite against it. For rollback, select a previously verified production deployment in Pages or rebuild the verified commit and redeploy. Review production after rollback. [Direct Upload documentation](https://developers.cloudflare.com/pages/get-started/direct-upload/) · [Pages rollbacks](https://developers.cloudflare.com/pages/configuration/rollbacks/)
