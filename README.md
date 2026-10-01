# kendi-ng.com

Kendi Ng's personal site and portfolio: marketing analytics, digital marketing and
the personal apps / Claude Code automations she builds. Plain HTML, CSS and vanilla JS,
no build step. Hosted on GitHub Pages at the custom domain in `CNAME` (`kendi-ng.com`).

## What is where

| Path | What it is |
|------|------------|
| `index.html` | Homepage: profile, skills, projects, career timeline, contact. |
| `project-list.html` | Full list of personal apps, automations and custom Claude Code skills. |
| `cv-analytics/` | CV, Data Analyst version (Python & ETL, AI integration, CRM analytics). |
| `cv-dm/` | CV, Digital Marketing version (SEO/SEM, paid ads, marketing analytics). |
| `claude-agents-model/` | Write-up of how agent tasks are routed to a chosen AI model by cost and reliability. |
| `miles-rebate-calculator/` | Standalone calculator: real cash-back value of redeeming frequent-flyer miles vs buying the ticket. |
| `backdoor/` | Unlinked site index of every live page (`noindex, nofollow`), kept in sync by hand. |
| `404.html` | Custom "page not found" page. |
| `assets/` | Shared `css/style.css`, `js/main.js` (nav toggle, smooth scroll, fade-in) and `images/` (CV PDF). |
| `CNAME` | Custom domain for GitHub Pages. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is, without Jekyll. |
| `PORTFOLIO_PROJECT_PLAN.md` | Original project plan the site was built from. |

Each folder page is a self-contained `index.html`; the CVs and homepage share `assets/`.

## Preview locally

```
python -m http.server 8000
```

from the repo root, then open <http://localhost:8000/>. Folder pages are at
`/cv-analytics/`, `/cv-dm/`, etc.

## Deploy rule

GitHub Pages publishes **`master`**: anything pushed there goes live on kendi-ng.com.

- Work on a branch, open a PR to `master`.
- Kendi merges. Nobody pushes to `master` directly.
- After a new page goes live, add it to `backdoor/index.html` so the site index stays complete.
