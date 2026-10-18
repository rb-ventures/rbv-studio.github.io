# rbv-studio.github.io

The website of RBV-Studio, the games brand of RB-Ventures LLC: https://rbv-studio.com (GitHub Pages from `main`, plain static HTML, no build step).

- `index.html`: the studio home; `assets/site.css`: the studio pages' styles
- `penguin-hotel-tycoon/`: the game's page and its pictures (`img/`, made by `roblox/tools/showcase.mjs` and `thumbs.mjs` in the game's repository)
- `parents/`, `support/`, `press/`, `privacy/`, `terms/`, `404.html`

Penguin Hotel Tycoon is public since 2026-10-18 (`data-live="true"`); a new game's page starts with `data-live="false"`, which shows "Opening soon" and points its Roblox buttons at the RBV-Studio community until it opens.

The logo (the windows of R and B lit like a hotel at dusk) is built by code: `python3 tools/logo/build_logo.py tools/logo/fonts/Fredoka.ttf assets/brand` writes `assets/brand/` (SVGs and press PNGs), the favicons, `apple-touch-icon.png` and `favicon.ico` (needs `resvg` and Pillow). Fredoka is under the SIL Open Font License (`tools/logo/fonts/OFL.txt`).


**Adding a game or app:** a folder `/<name>/` with its page (copy `/mypootime/` for an app or `/penguin-hotel-tycoon/` for a game), one card in `games/index.html` and, if it should be featured, the same card on the home page; a press-kit section and a parents/privacy line if it collects anything new. The menu stays Games · Parents · Support · Press.
