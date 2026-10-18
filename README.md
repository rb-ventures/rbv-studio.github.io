# rbv-studio.github.io

The website of RBV-Studio, the games brand of RB-Ventures LLC: https://rbv-studio.com (GitHub Pages from `main`, plain static HTML, no build step).

- `index.html`: the studio home; `assets/site.css`: the studio pages' styles
- `penguin-hotel-tycoon/`: the game's page and its pictures (`img/`, made by `roblox/tools/showcase.mjs` and `thumbs.mjs` in the game's repository)
- `parents/`, `support/`, `press/`, `privacy/`, `terms/`, `404.html`

The page says "Opening soon" while the game is private: set `data-live="true"` on `<html>` in `index.html` and `penguin-hotel-tycoon/index.html` when it goes public.
