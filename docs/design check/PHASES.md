# KrishiSetu phases: paste ONE at a time

Setup (once, by you, not the agent)
1. Copy `tokens.css` and `ndvi.js` to `frontend/src/styles/`. Copy `design-check.mjs` to `frontend/scripts/`.
2. Copy `GEMINI.md` (and `AGENTS.md`) to the repo root.
3. In `frontend/package.json` add to scripts: `"check": "node scripts/design-check.mjs"`.
4. `git commit` so every phase is one revertable step.

Prefix for every phase: "Read GEMINI.md first. Then do exactly this phase."

---

## Phase 0: cleanup (no visual change)
Touch: `frontend/src/components/`, `frontend/src/views/`, `frontend/src/router/index.js`
Do:
- Delete: components `AppHeader`, `CampaignOutput`, `EmptyState`, `HistoryList`, `MediaPreview`, `ResultsSkeleton`, `ScoreBand`; views `Onboarding`, `Inbox`, `Selfie`.
- Remove their imports and redirects from `router/index.js`. Keep the `/home`, `/dev-tool`, `/admin` redirects.
- Before deleting each file, `grep -r` its name in `src/` and show me the result.
Done when: `npm run check -- --phase 0` passes and `npm run build` succeeds. App looks identical.

## Phase 1: identity foundation
Touch: `index.html`, `src/main.js`, `src/styles.css`, `src/App.vue`
Do:
- `index.html`: replace the Archivo font link with
  `https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@400..800&family=Anek+Devanagari:wght@400..800&family=Anek+Latin:wght@400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap`
  (open the network tab once to confirm it returns 200). Set `theme-color` to `#EAF0DC`.
- `main.js`: first line `import './styles/tokens.css'`.
- `styles.css`: delete everything `tokens.css` now defines (the `:root` block, html/body, headings, buttons, badges, forms, `.card-solid`). Keep only skeleton, spin, footer, scrollbar. Zero hex; use tokens.
- `App.vue`: remove every hex and every font-size under 12px, replace `transition: all`, replace the `PhList` icon on the Sathi link with `PhPlant`. Nav labels: "Check a leaf", "Registry converter", "Outbreak watch" (small Bengali/Hindi label below is optional). Brand logo frame becomes `var(--sarson)` with a `var(--canopy)` icon.
Done when: `npm run check -- --phase 1` passes, build succeeds, all three routes still render.

## Phase 2: story page at `/` (static version first)
Touch: `src/router/index.js`, new `src/views/Story.vue`, `index.html`
Do:
- Routes: `/` -> Story, `/sathi` -> Home (keep `/home` redirect to `/sathi`). Update nav links.
- `Story.vue`: five full-width chapters, no scroll animation yet. Use `.band` (mustard) for chapter 1, plain paper for 2 to 4, `.band-dark` for 5.
  1. Hero. `.hero-title` (Bengali line then English line): "একটা পাতা থেকে একটা সীমান্ত" / "From one leaf to a whole border." Sub: "KrishiSetu spots crop disease early and warns the next district 48 hours ahead." Button "Check a leaf" -> `/sathi`.
  2. "Check a leaf": one sentence, link to `/sathi`.
  3. "Convert any state registry": one sentence, link to `/interop`.
  4. "Watch outbreaks cross borders": one sentence, link to `/command`.
  5. Dark band: the number "48 h" very large, caption "Head start for the next district." Button "Open outbreak watch".
- `index.html`: add `og:title`, `og:description`, `og:image` (`/og.png`, leave the file for later), `twitter:card` = summary_large_image.
- No gsap, no d3 in this phase.
Done when: `npm run check -- --phase 2` passes. (The animated scroll-zoom is added later from a scene file I will give you.)

## Phase 3: Outbreak watch (`views/Admin.vue`)
Touch: `src/views/Admin.vue` only
Do:
- Headings: h1 "Outbreak watch"; "Active trans-boundary outbreak vectors" -> "Outbreaks crossing borders"; "Agro-ecological interstate map" -> "Border map"; "Inject simulated outbreak event" -> "Simulate an outbreak".
- Page uses `.band-dark` for the map area, paper for the rest. Selected item uses `var(--sarson)`, outbreak uses `var(--alert-lite)` on dark, `var(--alert-text)` on light.
- Map: replace every hex in the SVG with tokens via `style="fill: var(--x)"` or classes. Map labels (the "Malda Hub (Active Outbreak)" text) must be generated from the `alerts` array, not typed in. Font sizes 12px minimum.
- KPI 24,580: bind to the data source if one exists, otherwise label it "Sample data".
- Replace pasted raw SVG icons with Phosphor.
Done when: `npm run check -- --phase 3` passes.

## Phase 4: Check a leaf (`views/Home.vue`)
Touch: `src/views/Home.vue`, new `src/components/sathi/*.vue`, new `src/styles/sathi.css`
Do:
- Order on screen: (1) leaf check (camera and voice buttons, 56px), (2) result, (3) field data, (4) treatment plan. The farmer profile ribbon becomes a slim line at the top, not a card.
- Copy: "Real-time environmental and orbital observation ledger" -> "Your field today"; "Specimen Intake & Observational Console" -> "Check a leaf"; "Verified diagnostic pathology and immediate action" -> "What it is and what to do now"; "Comprehensive agronomic management dossier" -> "Your treatment plan"; "Sync Environmental Telemetry" -> "Refresh field data".
- The humidity label: compute from the value against the 82% threshold ("Safe" below, "High risk" at or above). Class `alert` only when high risk.
- Split the file into section components. Move the scoped CSS into `sathi.css` using tokens only. `Home.vue` ends at 600 lines or fewer.
- No more than one dominant block per screen. Use `.unboxed` for at least two sections instead of `.card-solid`.
- Also fix Infographic components: no hex, no text under 12px.
Done when: `npm run check -- --phase 4` passes and the language dropdown still switches bn/hi/en.

## Phase 5: Registry converter (`views/DevTool.vue`)
Touch: `src/views/DevTool.vue`
Do:
- h1 "Registry converter". "1. Heterogeneous state-specific payload" -> "State registry data"; "2. Standardized FarmContext v1.0" -> "Standard FarmContext". State tabs are large pills (min 48px).
- On Convert: mapped fields highlight in `var(--sarson)` in the left panel and appear in the right panel, 900ms max, transform and opacity only. Skip the animation when `prefers-reduced-motion`.
- Tokens only, no hex, no text under 12px, Phosphor icons only.
Done when: `npm run check -- --phase 5` passes.

## Phase 6: share cards
Touch: new `src/components/ShareCard.vue`, `Admin.vue`, `Home.vue` (button only)
Do: install `html-to-image`. Build a 1080x1350 card (hidden until export): big local-language headline, district, risk level, next step, small app URL. "Share card" button on the diagnosis result and on each outbreak. Export PNG. Also run `npm run check -- --phase 6` (all files max 700 lines).

## Phase 7: QA
Run `npm run check -- --phase 7`, `npm run build`, Lighthouse (mobile) on `/`, `/sathi`, `/command`. Report scores. Fix accessibility issues only. Do not restyle.
