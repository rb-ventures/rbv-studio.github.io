# rbv-studio.github.io

The website of RBV-Studio, the games brand of RB-Ventures LLC: https://rbv-studio.com (GitHub Pages from `main`, plain static HTML, no build step).

- `index.html`: the studio home; `assets/site.css`: the studio pages' styles
- `penguin-hotel-tycoon/`: the game's page and its pictures (`img/`, made by `roblox/tools/showcase.mjs` and `thumbs.mjs` in the game's repository)
- `parents/`, `support/`, `press/`, `privacy/`, `terms/`, `404.html`

While the game is private the pages say "Opening soon" and their Roblox buttons lead to the public RBV-Studio community (a `when-soon` link; the game page itself answers "Content not accessible" to visitors). When it goes public, set `data-live="true"` on `<html>` in `index.html` and `penguin-hotel-tycoon/index.html`: the `when-live` links to the game show instead.

The logo (the windows of R and B lit like a hotel at dusk) is built by code: `python3 tools/logo/build_logo.py tools/logo/fonts/Fredoka.ttf assets/brand` writes `assets/brand/` (SVGs and press PNGs), the favicons, `apple-touch-icon.png` and `favicon.ico` (needs `resvg` and Pillow). Fredoka is under the SIL Open Font License (`tools/logo/fonts/OFL.txt`).
