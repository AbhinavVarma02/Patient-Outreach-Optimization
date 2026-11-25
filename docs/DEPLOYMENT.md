# Deployment

Deploy only a build that passed the publication check and browser test matrix. Pages Direct Upload serves web/dist with the bundled security headers. Current intended project slug is patient-outreach-optimization. Wrangler 4.168.0 was selected from the official npm package. Disable telemetry during release if required by the operator.

```sh
npm exec --yes --package=wrangler@4.168.0 -- wrangler whoami
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages project list
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages project create patient-outreach-optimization --production-branch main --force
npm exec --yes --package=wrangler@4.168.0 -- wrangler pages deploy web/dist --project-name patient-outreach-optimization --branch main
```

Run creation only when the verified account lacks that project. Wrangler 4.168.0 initially delegated creation to the Workers workflow and failed. The creation-only flag selected direct Pages creation. Deploys to the existing project use the ordinary Pages command. Confirm production domain and HTTPS response headers. Set OUTREACH_LIVE_URL to the verified URL and rerun the browser suite against it. For rollback, select a previously verified production deployment in Pages or rebuild the verified commit and redeploy. Review production after rollback. [Direct Upload documentation](https://developers.cloudflare.com/pages/get-started/direct-upload/) · [Pages rollbacks](https://developers.cloudflare.com/pages/configuration/rollbacks/)

| Release | Build commit | Production deployment ID | Verified deployment |
| --- | --- | --- | --- |
| v0.2.0-demo | `dad257536b358a5035f8f51f6da1719b4050fdd5` | `75a71ff8-c3c6-414b-b01c-12780f6dca7e` | [Deployment](https://75a71ff8.patient-outreach-optimization.pages.dev/) |
| v0.1.0-demo | `d988063bb75e2870ad8e26e2edf316919d81c6d6` | `9112bbb3-551f-4d76-b7a4-df4e99b1b976` | [Preserved deployment](https://9112bbb3.patient-outreach-optimization.pages.dev/) |

The stable production URL serves v0.2.0-demo. Both deployments' assets were verified after promotion. To roll back in Pages, select the earlier verified deployment ID for the same project. Additional external service cost was $0. [Stable production URL](https://patient-outreach-optimization.pages.dev/) · [Test and audit evidence](TEST_EVIDENCE.md)
