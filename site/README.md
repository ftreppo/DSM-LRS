# DSM-LRS public site

Static, dependency-free public site for the DSM-LRS project.

## Pages

- `index.html` — Welcome / project overview / architecture / start paths
- `manual.html` — multilingual User Manual
- `help.html` — multilingual Help & troubleshooting
- `data.js` — DE / IT / EN interface strings
- `app.js` — language selection only; no analytics or remote data access
- `styles.css` — responsive accessible presentation

## Privacy / runtime boundary

The site:
- requires no sign-in;
- includes no private Drive link;
- fetches no protected data;
- uses no tracker or analytics script;
- uses no external font;
- sets no cookie (language preference uses browser localStorage only);
- contains no student/member records.

The site is a public project surface, not an official DSM rulebook. Current individual arrangements and applicable school/examination rules prevail.

## Deployment

GitHub Pages deployment is defined in `.github/workflows/pages.yml` and publishes only this `site/` directory.
