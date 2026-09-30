# KrishiSetu phases: paste ONE at a time

Setup (once, by you, not the agent)
1. `frontend/src/styles/`: copy `tokens.css` and `ndvi.js`. `frontend/scripts/`: copy `design-check.mjs`.
2. Repo root: copy `GEMINI.md` and `AGENTS.md`. Create `design/` and copy `DESIGN.md`, `tokens.json`, `painting-prompt.md` into it.
3. `frontend/package.json` scripts: add `"check": "node scripts/design-check.mjs"`.
4. `git commit` so every phase is one revertable step.

Prefix for every phase: "Read GEMINI.md and design/DESIGN.md first. Then do exactly this phase."

---

## Phase 0: cleanup (no visual change)
Touch: `src/components/`, `src/views/`, `src/router/index.js`
- Delete components `AppHeader`, `CampaignOutput`, `EmptyState`, `HistoryList`, `MediaPreview`, `ResultsSkeleton`, `ScoreBand`; views `Onboarding`, `Inbox`, `Selfie`.
- Remove their imports and redirects from `router/index.js`. Keep the `/home`, `/dev-tool`, `/admin` redirects.
- `grep -r` each name in `src/` before deleting and show me the result.
Done when: `npm run check -- --phase 0` passes, build succeeds, app looks identical.

## Phase 1: identity foundation
Touch: `index.html`, `vite.config.js`, `src/main.js`, `src/styles.css`, `src/App.vue`
- `index.html`: replace the Archivo link with these two (keep the preconnects):
  `https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700&display=swap`
  `https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Noto+Serif+Bengali:wght@300;400;500&family=Noto+Serif+Devanagari:wght@300;400;500&family=Anek+Bangla:wght@400;500;600&family=Anek+Devanagari:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`
  Open the network tab once: both must return 200 and Bengali text must render. Set `theme-color` to `#0E7AA3`.
- `vite.config.js`: add a `CacheFirst` runtime cache for `^https:\/\/(api|cdn)\.fontshare\.com\/.*` next to the existing font caches. Manifest `theme_color` `#0E7AA3`, `background_color` `#FFFFFF`.
- `main.js`: first line `import './styles/tokens.css'`.
- `styles.css`: delete everything `tokens.css` now defines (`:root`, html/body, headings, buttons, badges, forms, `.card-solid`). Keep only skeleton, spin, footer, scrollbar, recoloured with tokens. Zero hex.
- `App.vue`: nav becomes a solid `.sky` bar. Logo badge: 1px white border, sprout icon plus wordmark, white. Links white 15px/500; active link gets a 1.5px `var(--color-haze)` pill outline. Online/offline switch stays a pill. Replace `PhList` with `PhPlant`. Nav labels: "Check a leaf", "Registry converter", "Outbreak watch". Footer on white, hairline top. Remove every hex, font-size under 12px, `transition: all`.
Done when: `npm run check -- --phase 1` passes; all three routes render; nav readable.

## Phase 2: story page at `/`
Touch: `src/router/index.js`, `src/App.vue` (one class toggle), new `src/views/Story.vue`, `index.html`
- Routes: `/` -> Story (name `story`), `/sathi` -> Home. Keep `/home` redirect to `/sathi`. Update nav links. On the `story` route, add class `nav-transparent` (position absolute, transparent) so the nav sits on the hero.
- `Story.vue`, in this order, no scroll animation:
  1. `.sky-hero` with `data-risk="clear"`. `.display` line 1 (Bengali): "একটা পাতা থেকে একটা সীমান্ত". Line 2: "From one leaf to a whole border." Sub, 18px white: "KrishiSetu spots crop disease early and warns the next district 48 hours ahead." Buttons: `.btn-gov-primary` "Check a leaf" with `PhArrowRight`, `.btn-gov-outline` "See outbreaks".
  2. `.quiet`: row of three `.card-solid` (24px gap, wraps on mobile): "Check a leaf" / "Photograph a leaf or speak. Get the disease and what to do today." link to `/sathi`; "Convert any registry" / "Bring state records into one standard format." link to `/interop`; "Watch outbreaks" / "See disease cross district borders before it reaches your field." link to `/command`. Card title is h2 (serif), link is `.btn-gov-outline`.
  3. `.sky` with `data-risk="storm"`: `.display` "48 hours", 18px white "Head start for the next district.", `.btn-gov-primary` "Open outbreak watch" (it inverts to white automatically).
- Do not add images. The painting is added later by setting `--hero-art` once `public/art/` has files.
- `index.html`: add `og:title`, `og:description`, `og:image` (`/og.png`, file added later), `twitter:card` = summary_large_image.
- No gsap, no d3.
Done when: `npm run check -- --phase 2` passes. (Bengali line is a placeholder; I will replace it.)

## Phase 3: Outbreak watch (`views/Admin.vue`)
Touch: `src/views/Admin.vue` only
- Start with `.sky.sky-strip` holding h1 "Outbreak watch" and a status line generated from `alerts` ("3 outbreaks active. 1 crosses a border."). `:data-risk`: `storm` if any alert is high or critical, `watch` if any alert exists, else `clear`. Check the alert data shape first and use the real severity field.
- Below: a `.desk` of white cards. KPIs as Field Data Cards. Corridors as Diagnosis Rows (paddy-mist). Renames: "Active trans-boundary outbreak vectors" -> "Outbreaks crossing borders"; "Agro-ecological interstate map" -> "Border map"; "Inject simulated outbreak event" -> "Simulate an outbreak".
- Map: `.card-float` white card; map ground `var(--color-storm)`, state shapes `var(--color-deep-monsoon)` and `var(--color-canopy-hover)`, border `var(--color-haze)`, outbreak `var(--color-chilli)` with a white ring, threatened `var(--color-straw-fill)`, labels white 12px or larger. Use classes or `style="fill: var(--x)"`. Map labels (the "Malda Hub (Active Outbreak)" text) come from `alerts`, not typed in.
- KPI 24,580: bind to data if a source exists, otherwise label "Sample data".
- Simulate modal: white, radius 20px, `--shadow-lift`, pill buttons.
- Replace pasted SVG icons with Phosphor.
Done when: `npm run check -- --phase 3` passes.

## Phase 4: Check a leaf (`views/Home.vue`)
Touch: `src/views/Home.vue`, new `src/components/sathi/*.vue`, new `src/styles/sathi.css`
- Start with `.sky.sky-strip`: h1 = farmer name (serif), status line from humidity ("Humidity is high. Check the lower leaves today."), small tags for district and crop. `:data-risk` from humidity through one constant `HUMIDITY_RISK = { watch: 70, storm: 82 }`. 82 is the existing fungal threshold marker; 70 is my placeholder, so read `backend/data/agronomy_knowledge.jsonl` and tell me if it disagrees.
- Then a `.desk`, in this order: (1) "Check a leaf" card with camera and voice as `.btn-xl`; (2) "What it is and what to do now"; (3) "Your field today" as Field Data Cards; (4) "Your treatment plan". The farmer profile ribbon becomes the strip; delete the card.
- Copy: "Real-time environmental and orbital observation ledger" -> "Your field today"; "Specimen Intake & Observational Console" -> "Check a leaf"; "Verified diagnostic pathology and immediate action" -> "What it is and what to do now"; "Comprehensive agronomic management dossier" -> "Your treatment plan"; "Sync Environmental Telemetry" -> "Refresh field data".
- Humidity label: computed from the value against `HUMIDITY_RISK` ("Safe", "Watch", "High risk") as a status pill. Remove the hard-coded "(Elevated)".
- On language change also set `document.documentElement.lang` to `bn`, `hi` or `en`.
- Split into section components; move scoped CSS to `sathi.css` using tokens. `Home.vue` ends at 600 lines or fewer. Fix Infographic components too: no hex, no text under 12px. Status colours there use `--color-leaf`, `--color-straw-fill`, `--color-chilli`.
Done when: `npm run check -- --phase 4` passes and the language dropdown still switches bn/hi/en.

## Phase 5: Registry converter (`views/DevTool.vue`)
Touch: `src/views/DevTool.vue`
- `.sky.sky-strip` (clear) with h1 "Registry converter". `.desk` with two white cards: "State registry data" (was "1. Heterogeneous state-specific payload") and "Standard FarmContext" (was "2. Standardized FarmContext v1.0"). Code panes use `var(--inkwell)` and `--font-mono`.
- State tabs are pills, min 48px: selected = canopy fill, others outlined.
- On Convert, mapped rows highlight (paddy-mist) in the left card and appear in the right card, 900ms max, transform and opacity only. No animation under `prefers-reduced-motion`.
Done when: `npm run check -- --phase 5` passes.

## Phase 6: share cards
Touch: new `src/components/ShareCard.vue`, `Admin.vue` and `Home.vue` (button only)
- Install `html-to-image`. Hidden 1080x1350 card: `.sky` background by risk, white `.card-float` with serif headline in the user's language, district, risk pill, next step, small URL. Await `document.fonts.ready` before export so Bengali and Hindi render. "Share card" button on the diagnosis result and on each outbreak. Export PNG.
- Run `npm run check -- --phase 6` (all `.vue` files max 700 lines).

## Phase 7: QA
Run `npm run check -- --phase 7`, `npm run build`, Lighthouse (mobile) on `/`, `/sathi`, `/command`. Confirm offline reload still shows Switzer and Cormorant (service worker caching). Report scores. Fix accessibility only. Do not restyle.
