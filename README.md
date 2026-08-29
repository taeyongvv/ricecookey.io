# ricecookey.io

The official website for **RiceCookey** — a small independent studio crafting
indie games and lifestyle apps. Static site, no build step, ready for GitHub Pages.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole page (hero, what we make, studio, contact). |
| `styles.css` | Styling — toasted "rice cookie" palette; games = coral, apps = green. |
| `script.js` | Scroll reveals + AJAX contact form. |
| `analytics.js` | Privacy-minimal pageview tracking for the Ricecookey dashboard. |
| `rakunovel/privacy/` | Rakunovel privacy policy. |
| `rakunovel/terms/` | Rakunovel terms of service. |
| `.nojekyll` | Tells GitHub Pages to serve files as-is. |

## Run locally

It's plain HTML/CSS/JS — just open `index.html`, or:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy to GitHub Pages

1. Push these files to the `main` branch.
2. The `Deploy static site to Pages` GitHub Actions workflow uploads the repository root and deploys it.
3. Your site goes live at `https://taeyongvv.github.io/ricecookey.io/`.

### Custom domain (ricecookey.io)
If you own the domain, add a file named `CNAME` containing one line — `ricecookey.io` —
then point the domain's DNS at GitHub Pages and set the custom domain in Settings → Pages.

## Contact form

The form uses [FormSubmit](https://formsubmit.co) — no backend, no signup.
**One-time activation:** the first time someone submits the form (or you submit it
yourself once), FormSubmit emails `ricecookey.official@gmail.com` with a confirmation
link. Click it once, and every message after that arrives in your inbox.

To hide the email address from scrapers, you can later swap the address in
`index.html` and `script.js` for the random token FormSubmit gives you after activation.
