# KrishiSetu Redesign: Master Prompt

Paste everything below the line into Claude Code (run from the repo root). Work phase by phase; do not skip the plan step.

---

## Role

You are the design lead and front-end engineer for KrishiSetu, an open-source agri Digital Public Good. Your job is to give the Vue frontend a distinctive, memorable, shareable visual identity without breaking any working behaviour.

## Product context

- Stack: Vue 3, Vite, vue-router, Chart.js, Phosphor icons, vite-plugin-pwa. Frontend lives in `frontend/`. Do not touch `backend/`.
- Three portals: **Kisan Sathi** (farmer diagnosis, Bengali/Hindi/English, voice, offline), **Kisan Setu** (registry interoperability studio), **Kisan Rakshak** (regional outbreak command, Malda to Katihar corridor, 48 h warning lead).
- Audiences, in order: (1) jury and government stakeholders on a laptop, watching a 90-second demo; (2) extension officers; (3) smallholder farmers on low-end Android, often in bright sun, often offline.
- Current problem: `frontend/src/styles.css` bans gradients, shadows, glow and motion beyond a 240 ms opacity fade. Every panel is the same `.card-solid`. There is no landing page, no focal point, no story. Headings are system-speak. The result reads as a government form.

## Design direction: "Field to Satellite"

The product's true story is a zoom: a lesion on one leaf, a field, a district, a state border, the satellite view where a pathogen crosses it 48 hours before anyone sees it. The identity is built from that story. Bold flat colour like a printed poster, one big scroll moment, and honest data graphics.

### Tokens (replace the `:root` block; keep old alias names mapped to new values so views don't break)

```css
:root {
  --sarson:      #F4C21F; /* mustard. Fill only: hero fields, primary button, highlights. Never text on light. */
  --canopy:      #0C3B2B; /* primary text, dark surfaces */
  --paddy-wash:  #EAF0DC; /* page background */
  --leaf:        #1F6B3A; /* healthy state, links, text-safe green */
  --leaf-bright: #2F8F4E; /* graphics and large text only */
  --soil:        #5B3A29; /* secondary text, earth accents */
  --alert:       #E8462A; /* outbreak only. Shapes and large bold text. */
  --alert-lite:  #FF7A5C; /* alert on dark surfaces */
}
```

Verified contrast: canopy on paddy-wash 10.74, canopy on sarson 7.51, white on canopy 12.53, leaf on paddy-wash 5.58, soil on paddy-wash 8.64, alert-lite on canopy 4.89. Do NOT use: leaf-bright as body text (3.49), alert as body text on light (3.37) or on canopy (3.19), sarson text on light (1.43), white on alert below 24 px / 18.66 px bold (3.93).

Gradients are allowed in exactly one place: the NDVI ramp (soil `#7A4A2B` → straw `#D9B54A` → leaf `#6BBF3B` → canopy `#0B7A4B`), because it encodes real Sentinel-2 data. No decorative gradients, no gradient text, no glassmorphism, no purple.

### Type

- One family for display and body: **Anek** (Anek Latin, Anek Bangla, Anek Devanagari). Same design across all three scripts, variable weight and width. Display: wdth 75 to 100, weight 700 to 800, tight tracking. Body: wdth 100, weight 400 to 500.
- **IBM Plex Mono** for data only: NDVI values, coordinates, granule IDs, schema keys.
- Self-host subsetted woff2 (Latin, Bengali, Devanagari), preload the display file, `font-display: swap`. Total font budget 150 KB. This also fixes first-load-offline, since fonts are currently runtime-cached from Google.
- Scale: base 17 px (16 px min on mobile), then 20 / 24 / 32 / 48 / clamp(56px, 9vw, 120px) for hero. Nothing under 12 px anywhere; Home.vue currently has 34 declarations at 10 to 13 px. Fix them.
- Line length under 70 characters. No all-caps eyebrow above every heading. No `A · B · C` meta strings. No "→" on every button.

### Copy rules

Plain verbs, sentence case, name things by what the person does. One job per element. Examples of the rewrite to apply (technical names stay as small secondary text):

| Now | Becomes |
|---|---|
| Real-time environmental and orbital observation ledger | Your field today |
| Specimen Intake & Observational Console | Check a leaf |
| Verified diagnostic pathology and immediate action | What it is and what to do now |
| Comprehensive agronomic management dossier | Your treatment plan |
| Kisan Rakshak: regional outbreak command center | Outbreak watch |
| Kisan Setu: cross-state interoperability console | Registry converter |
| Sync Environmental Telemetry | Refresh field data |

Bengali and Hindi labels are first-class: every new string needs `bn` and `hi` versions wherever the existing view already localises.

## Information architecture

```
/            NEW  Story page: scroll-zoom hero, 3 chapters (one per portal), the 48 h number, CTA
/sathi       was "/"  Farmer tool (Home.vue). Keep /home redirect -> /sathi
/interop     Registry converter (DevTool.vue)
/command     Outbreak watch (Admin.vue)
```

Nav: logo, Sathi, Setu, Rakshak, online/offline switch. Update `router/index.js`, `App.vue`.

## Signature moments (spend boldness here, keep everything else quiet)

1. **Story hero (the one memorable thing).** Full-viewport, mustard field. Headline in huge Anek Bangla/Latin. On scroll, a pinned SVG scene zooms out in 5 stages: leaf lesion, paddy rows, NDVI mosaic, district outlines, the WB/Bihar border with the Malda to Katihar vector animating and a live "48 h" counter. The last frame is the same visual as the Outbreak watch map. Use GSAP + ScrollTrigger (scrub). Provide a static stacked fallback for `prefers-reduced-motion` and for viewports under 640 px or `navigator.connection.saveData`.
2. **Outbreak map (the working centrepiece).** Replace the hand-drawn polygons in `Admin.vue` with real simplified district GeoJSON (Malda, Murshidabad, Nadia, Katihar, Purnia, Kishanganj; use open district boundaries such as DataMeet's, verify licence, simplify with mapshaper to under 60 KB). Render with d3-geo into SVG. Choropleth by outbreak intensity on the NDVI ramp, dark canopy surface (functional dark), animated dashed particle flow along the transmission vector, hover for district detail. Remove all hard-coded hex values from the map; use tokens.
3. **Shareable Border Alert card and Diagnosis card.** A button exports a 1080x1350 PNG (html-to-image or canvas) sized for WhatsApp: big Bengali/Hindi headline, district, risk, next step, tiny QR to the app. This is the real virality mechanic in this market.

Per-portal temperature, one system:
- **Sathi**: daylight, largest type, photo-first. Big camera and voice buttons (min 56 px tall). No motion beyond user-triggered feedback. Sun-readable contrast.
- **Setu**: the "bridge". Left: messy state payloads (WB, BR, OD). Right: canonical FarmContext. On convert, field keys visibly travel and snap into the standard schema (short, user-triggered, under 900 ms).
- **Rakshak**: dark canopy surface, mustard for selection, alert for outbreak only.

Hierarchy rule: no more than one dominant block per screen. Replace the uniform `.card-solid` stack with three levels: a full-bleed hero band, standard panels, and unboxed content on the page background. Vary radius by role (0 on bands, 16 on panels, pill on buttons).

## Motion rules

One orchestrated hero sequence plus responses to user actions (open, expand, convert, export, confirm). No fade-up on every section. No hover lift on every card. Respect `prefers-reduced-motion`. Animate transform and opacity only.

## Constraints (do not break)

- Preserve all API calls, composables (`useOfflineStorage`, `useRealtimeSync`, `useTheme`, etc.), IndexedDB offline behaviour, PWA build, and `v-text` bindings.
- Landing page adds at most 60 KB gzipped JS. Sathi route must not load GSAP or d3-geo.
- Target: LCP under 2.5 s on throttled 4G, mid-range Android. Lighthouse accessibility 95+.
- WCAG AA: visible keyboard focus, real button/label semantics, colour never the only signal.
- Add to `index.html`: `og:title`, `og:description`, `og:image` (1200x630, generated from the hero), `twitter:card`, correct `theme-color`.
- The repo's `ux-lint` ruleset will flag this direction (it bans gradients, shadows and glow). Update the ruleset to allow the NDVI ramp and functional dark surfaces; do not water the design down to satisfy it.

## Cleanup (Phase 0, verify each with grep before deleting; ask me if unsure)

- Unused components carrying a different product's branding ("Terrapulse"): `AppHeader.vue`, `CampaignOutput.vue`, `EmptyState.vue`, `HistoryList.vue`, `MediaPreview.vue`, `ResultsSkeleton.vue`, `ScoreBand.vue`.
- Views imported in the router but only redirected: `Onboarding.vue`, `Inbox.vue`, `Selfie.vue`. Confirm nothing live depends on them (`Analytics`, `Explainability`, `FarmerForm`, `ToastStack` are referenced by them), then remove.
- `Home.vue` is 3,494 lines with about 2,145 lines of scoped CSS and hard-coded hexes. Extract repeated patterns into `src/styles/` (tokens, type, layout, components) and split Home into section components as you restyle. Do not restyle by editing tokens alone; scoped CSS will ignore them.

## Process (follow exactly)

1. **Plan first.** Before writing code, output: token table, type scale, ASCII wireframes for `/`, `/sathi`, `/command` (desktop and mobile), the file-by-file change list. Then critique your own plan against this brief: if any part looks like what you would produce for any farming or dashboard site, revise it and say what you changed. Wait for my "go".
2. Execute one phase at a time. After each phase: `npm run build`, run the app, screenshot each changed route at 1440 px and 390 px, fix what you see, then show me the screenshots and a 5-line changelog.
3. Do not start the next phase until I approve.

## Phases and acceptance criteria

| # | Phase | Done when |
|---|---|---|
| 0 | Cleanup and structure | Dead files removed, build passes, no visual change |
| 1 | Tokens, type, self-hosted fonts, base components | Every view uses new tokens; no hard-coded hex outside the NDVI ramp; base font 17 px; fonts self-hosted |
| 2 | Story page `/` and routing | Scroll-zoom works at 60 fps on desktop, static fallback on mobile and reduced-motion; OG tags live |
| 3 | Outbreak watch | Real GeoJSON map, animated vector, tokenised colours, hover detail, 48 h counter |
| 4 | Kisan Sathi | Rewritten headings, 56 px touch targets, hierarchy of one dominant block, Bengali/Hindi checked |
| 5 | Registry converter | Convert animation under 900 ms, works with keyboard, reduced-motion variant |
| 6 | Share cards | Both cards export a correct 1080x1350 PNG in bn, hi, en |
| 7 | QA | Lighthouse a11y 95+, LCP target met, offline reload works, no console errors |

## Kill list

Glassmorphism, gradient headlines, purple/blue SaaS palette, identical rounded cards everywhere, emoji as icons, stock farmer photos, decorative blobs, scatter fade-ups, tiny grey 11 px text, cream background with terracotta accent, near-black background with a single neon accent.
