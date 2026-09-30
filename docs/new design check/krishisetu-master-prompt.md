# KrishiSetu Redesign: Master Prompt (v2, "Sky over the paddy")

For Claude Code or any capable agent, run from the repo root. Weaker agents: use `GEMINI.md` plus one phase from `PHASES.md` at a time instead of pasting this.

---

## Role

You are design lead and front-end engineer for KrishiSetu, an open-source agri Digital Public Good. Give the Vue frontend a distinctive, memorable, shareable identity without breaking working behaviour.

## Source of truth

`design/DESIGN.md` (style reference), `frontend/src/styles/tokens.css`, `design/tokens.json`, `frontend/src/styles/ndvi.js`, `design/painting-prompt.md`. Read DESIGN.md fully before proposing anything. Do not re-derive the palette, type or components; extend them only where the spec is silent, and say so.

## Product context

- Stack: Vue 3, Vite, vue-router, Chart.js, Phosphor icons, vite-plugin-pwa. Frontend in `frontend/`. Do not touch `backend/`.
- Portals: **Kisan Sathi** (`/sathi`, farmer diagnosis, Bengali/Hindi/English, voice, offline), **Kisan Setu** (`/interop`, registry converter), **Kisan Rakshak** (`/command`, outbreak watch, Malda to Katihar corridor, 48 h warning lead).
- Audiences in order: jury on a laptop in a 90-second demo; extension officers; smallholders on low-end Android in bright sun, often offline.
- Problem being solved: the old system banned gradients, shadows and motion, and every panel was the same flat card. It read as a government form with no focal point or story.

## Design direction

The style is adapted from the Cora reference: a painted sky as the canvas with text sitting directly on it, white cards floating on quiet sections, light serif over neutral sans, pill actions, tinted two-direction shadows, one accent. For farming:

- The painting is a monsoon sky over the Bengal delta (mango tree, paddy, palms, egrets, a far bamboo footbridge for "setu"). Sky states clear, overcast and storm follow the data through `data-risk`.
- Palette: monsoon-sky, canopy pill, chilli accent. Leaf and straw exist as status ink only.
- Type: Switzer + Anek (UI), Cormorant Garamond + Noto Serif Bengali/Devanagari (display). Body 17px. Indic text gets 1.35 heading and 1.65 body leading.
- Accessibility fixes over Cora: muted greys darkened, sky outlines lightened, primary pill darkened and inverted on storm sky.

## Information architecture

```
/         Story: sky hero, three cards, "48 hours" sky section
/sathi    Check a leaf (was "/"). Keep /home redirect
/interop  Registry converter
/command  Outbreak watch
```

## Signature moments (spend boldness here, keep everything else quiet)

1. **The sky.** Story hero uses the painting (gradient fallback until the image exists). The same painting in three weather states is reused on the share cards. App routes use the CSS gradient strips, not the image, to protect performance.
2. **Outbreak watch.** Header sky follows alerts. Map card: storm-coloured ground, districts on the NDVI ramp, outbreak in chilli, animated dashed vector along the transmission path. Replace the hand-drawn polygons with simplified district GeoJSON (Malda, Murshidabad, Nadia, Katihar, Purnia, Kishanganj; open boundary data such as DataMeet's, verify licence, simplify under 60 KB, render with d3-geo). Labels come from data.
3. **Share cards.** 1080x1350 PNG (sky by risk, white float card, serif headline in the farmer's language) for WhatsApp. This is the real virality mechanic in this market.

Optional, only after phase 7 and only on `/`: a scroll descent that moves three painting layers at different rates using CSS scroll-driven animation, with a static fallback. No GSAP.

## Constraints

- Preserve all API calls, composables, IndexedDB offline behaviour, PWA build, `v-text` bindings.
- Story route adds at most 60 KB gzipped JS. `/sathi` loads no d3-geo.
- LCP under 2.5 s on throttled 4G, mid-range Android. Lighthouse accessibility 95+.
- WCAG AA. Colour is never the only signal: every status pill carries a word.
- Set `document.documentElement.lang` on language change.
- Fonts must work offline: cache Fontshare and Google font requests in the service worker, or self-host in phase 7.
- `index.html`: `og:title`, `og:description`, `og:image`, `twitter:card`, `theme-color #0E7AA3`.
- The old `ux-lint` ruleset bans gradients and shadows. Update it to allow the token shadows and `--sky-*` gradients; do not weaken the design to satisfy it.

## Process

1. **Plan first.** Output the file-by-file change list and ASCII wireframes for `/`, `/sathi`, `/command` (desktop and mobile). Critique it against DESIGN.md: if any part could belong to any farming dashboard, revise and say what changed. Wait for my "go".
2. One phase at a time (`PHASES.md`). After each: `npm run check -- --phase N`, `npm run build`, screenshots of changed routes at 1440px and 390px, 5-line changelog. Wait for approval.

## Phases

| # | Phase | Done when |
|---|---|---|
| 0 | Cleanup | Dead files removed, build passes, no visual change |
| 1 | Tokens, fonts, base, nav | No hex outside tokens, Bengali renders, nav readable |
| 2 | Story page and routing | Sky hero, card row, "48 hours" section, OG tags |
| 3 | Outbreak watch | Data-driven sky, tokenised map, no literal status |
| 4 | Check a leaf | One dominant block, computed humidity label, `lang` set, Home under 600 lines |
| 5 | Registry converter | Convert animation under 900 ms, reduced-motion safe |
| 6 | Share cards | Correct PNG in bn, hi, en |
| 7 | QA | Lighthouse a11y 95+, offline fonts OK |

## Kill list

Glassmorphism, blur, scrims over the sky, gradient headlines, purple or fintech blue, extra accent hues, identical cards everywhere, emoji icons, stock farmer photos, decorative blobs, scattered fade-ups, serif on buttons or body, reduced-opacity text on sky, leading under 1.3 on Indic text.
