# johnmolendyk.com

Static site for GitHub Pages. Content lives in `build.py`; styles in `assets/style.css`.

## Update the site
1. Edit text in `build.py` (case studies, home, approach, about, contact).
2. Run `python3 build.py .` to regenerate the pages.
3. Commit and push. GitHub Pages publishes automatically.

## Before going live
- Replace `YOUR_WEB3FORMS_ACCESS_KEY` in `build.py` (the key flowhaus.ai uses works).
- Verify the case-study figures flagged in the hand-off notes.
- DNS: point the apex and `www` records at GitHub Pages. Do not touch MX records or email stops.
- Cancel the Webflow hosting plan only after the new site is live.

## Lab section
`/lab/` (Insights, AI Register) is built but hidden: not in the nav, footer or sitemap, and marked noindex.
When the text is real, set `SHOW_LAB = True` in `build.py`, rebuild and push.
Screenshots go in `assets/lab/`. Redact names, emails, keys and internal URLs first.
