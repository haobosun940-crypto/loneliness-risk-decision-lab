# Custom Domain Deployment Guide

This project can be moved from the GitHub Pages URL to a normal custom domain such as:

```text
https://www.lonelinessriskdecisionlab.com
```

## Recommended Path: Netlify Static Hosting

Use this if the goal is a normal public website with a custom `www` domain and downloadable research assets.

1. Buy a domain from a registrar such as Cloudflare Registrar, Namecheap, GoDaddy, Alibaba Cloud, Tencent Cloud, or another provider.
2. Open Netlify and choose **Add new project**.
3. Choose **Import an existing project** and connect this GitHub repository:

```text
https://github.com/haobosun940-crypto/loneliness-risk-decision-lab
```

4. Use these build settings:

```text
Build command: python3 scripts/build_root_static_site.py
Publish directory: dist
```

The same settings are already saved in `netlify.toml`, so Netlify should detect them automatically.

5. After the first deploy works, open **Domain management** and add:

```text
www.lonelinessriskdecisionlab.com
```

6. In the domain DNS provider, create the DNS record Netlify asks for. It is usually a `CNAME` record for `www`.
7. Wait for DNS and HTTPS certificate provisioning to finish.

## Alternative: Cloudflare Pages

Use this if the domain is also managed in Cloudflare.

1. Open Cloudflare Pages.
2. Connect the GitHub repository.
3. Use:

```text
Build command: python3 scripts/build_root_static_site.py
Build output directory: dist
```

4. Add a custom domain in Cloudflare Pages and point `www` to the Pages project.

## Important Data Note

This static deployment preserves:

- the visual website
- the questionnaire route
- personal scoring in the browser
- static dashboard data
- CSV export
- PDF, Word, PPT, Excel, video, and ZIP downloads

It does not create a central public database for new submissions. Browser-only submissions remain in the visitor's browser session unless a real backend API is deployed.

For central data collection, deploy `server.py` as a backend service and connect `static/app.js` through `page-config.js` with an API base URL. The existing `render.yaml` is already prepared for this backend path.

## Domain Choice

Good project-style domains:

```text
lonelinessriskdecisionlab.com
lonelinessdecisionlab.com
socialrisklab.com
riskdecisionlab.com
lrdlab.com
```

For a formal school/research presentation, the first two names are the clearest.
