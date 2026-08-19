# LiftLog

A single-file workout tracker built for Bryce's 6-day split. No server, no accounts —
all data lives in the browser's localStorage on your device.

**Live app:** https://brutkiew.github.io/liftlog/

## Install on your phone

- **iPhone (Safari):** open the link → Share → **Add to Home Screen**
- **Android (Chrome):** open the link → ⋮ menu → **Install app** / Add to Home screen

Works offline after the first load.

## What's inside

- `index.html` — the whole app (schedule, logging, progression, PRs, trends, heat map, AI coach)
- `manifest.webmanifest` + `icons/` — PWA install bits
- `sw.js` — service worker for offline use
- `make_icons.py` — regenerates the icons (needs Pillow)

Your training data never leaves the device. Use **Settings → Backup** to export a JSON
copy, and **Restore** to load it on another device.
