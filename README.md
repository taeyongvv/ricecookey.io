# ricecookey.io

The official website for **RiceCookey** — a small independent studio crafting
indie games and lifestyle apps. Static site, no build step, ready for GitHub Pages.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole page (hero, what we make, studio, contact). |
| `styles.css` | Styling — toasted "rice cookie" palette; games = coral, apps = green. |
| `script.js` | Scroll reveals + AJAX contact form. |
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

## X campaign links

| App | Android | iOS |
| --- | --- | --- |
| 식집사 | https://www.ricecookey.com/go/plants/x/aos/ | https://www.ricecookey.com/go/plants/x/ios/ |
| 겸사겸사 | https://www.ricecookey.com/go/gyeomsa/x/aos/ | https://www.ricecookey.com/go/gyeomsa/x/ios/ |

The original `/go/{app}/{aos,ios}/` links remain unchanged. The `x` path
separates X-link visits in Vercel Web Analytics without paid UTM breakdowns.
These are link visits, not downloads; shared links, previews, blockers, and QA
traffic can affect counts. The existing 350 ms redirect is best-effort, not a
receipt guarantee. The three-second meta refresh and manual link still work.

Android passes the percent-encoded Install Referrer payload
`utm_source=x&utm_medium=social&utm_campaign=x`. This alone does not implement
first-open attribution: the app must retrieve and record the Install Referrer.
No app binary, SDK, consent flow, or paid service was changed.

iOS currently tracks **X-link visits only** and redirects to the original store
URL without campaign parameters. App Store Connect browser authentication is
required to obtain a verified developer provider token; never substitute a
Team ID, vendor number, app ID, or a made-up token. Once obtained from an
existing/generated campaign link, add `pt=<verified token>&ct=x&mt=8` to all
three destinations (meta refresh, anchor, JavaScript) in each X iOS page and
update the checker. Do not describe iOS campaign downloads as enabled before
that step. Apple's campaign reporting also has minimum sample thresholds.

Checks (stdlib only):

```sh
python3 scripts/check_tracking_links.py
python3 scripts/check_tracking_links.py https://www.ricecookey.com
```

## Contact form

The form uses [FormSubmit](https://formsubmit.co) — no backend, no signup.
**One-time activation:** the first time someone submits the form (or you submit it
yourself once), FormSubmit emails `ricecookey.official@gmail.com` with a confirmation
link. Click it once, and every message after that arrives in your inbox.

To hide the email address from scrapers, you can later swap the address in
`index.html` and `script.js` for the random token FormSubmit gives you after activation.
