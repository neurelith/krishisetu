#!/usr/bin/env node
// KrishiSetu design gate. Run from frontend/:  node scripts/design-check.mjs --phase N [--all]
// Exit code 1 = a rule failed. The agent may not say "done" until this prints PASS.
import fs from 'node:fs'
import path from 'node:path'

const argv = process.argv.slice(2)
const pi = argv.indexOf('--phase')
const phase = pi >= 0 ? Number(argv[pi + 1]) : 1
const showAll = argv.includes('--all')
const SRC = path.resolve('src')
const INDEX = path.resolve('index.html')

const walk = (d) => fs.existsSync(d) ? fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? (e.name === 'node_modules' ? [] : walk(path.join(d, e.name))) : [path.join(d, e.name)]) : []
const files = walk(SRC).filter((f) => /\.(vue|css|js)$/.test(f)).map((f) => ({
  rel: path.relative(SRC, f).split(path.sep).join('/'), text: fs.readFileSync(f, 'utf8') }))
const read = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '')
const exists = (rel) => fs.existsSync(path.join(SRC, rel))

// Files that must be fully clean once their phase is reached (cumulative).
const CLEARED = [[1, /^(App\.vue|styles\.css|styles\/)/], [3, /^views\/Admin\.vue$/],
  [4, /^(views\/Home\.vue|components\/)/], [5, /^views\/DevTool\.vue$/]]
const cleared = (rel) => CLEARED.some(([p, re]) => phase >= p && re.test(rel))
const ALLOW_RAW = /^styles\/(tokens\.css|ndvi\.js)$/

const results = []
const rule = (id, from, fn) => { if (phase >= from) results.push({ id, hits: fn() }) }
const scan = (re, msg, { skip = () => false, test = (m) => true } = {}) => {
  const hits = []
  for (const f of files) {
    if (!cleared(f.rel) || skip(f.rel)) continue
    f.text.split('\n').forEach((line, i) => {
      for (const m of line.matchAll(re)) if (test(m)) { hits.push(`${f.rel}:${i + 1}  ${msg(m)}`); break }
    })
  }
  return hits
}

rule('HEX_OUTSIDE_TOKENS', 1, () => scan(/(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?!\w)/g,
  (m) => `raw colour ${m[0]}. Use var(--token).`, { skip: (r) => ALLOW_RAW.test(r) }))

rule('FONT_UNDER_12PX', 1, () => scan(/font-size:\s*(\d*\.?\d+)(px|rem)/g,
  (m) => `font-size ${m[1]}${m[2]} is below the 12px floor. Use .meta or a --step-* token.`,
  { test: (m) => (m[2] === 'px' ? +m[1] < 12 : +m[1] < 0.75) }))

rule('NO_BLUR_OR_GLOW', 1, () => [
  ...scan(/backdrop-filter|filter:\s*blur|text-shadow/g, (m) => `"${m[0]}" is not allowed. The sky is never blurred, frosted or overlaid.`),
  ...scan(/box-shadow:\s*([^;]+)/g, () => 'raw box-shadow. Use var(--shadow-card), var(--shadow-float) or var(--shadow-lift).', {
    test: (m) => { const n = m[1].split(',')[0].trim().split(/\s+/).filter((t) => /^-?\d*\.?\d+(px)?$/.test(t)).map(parseFloat); return n.length >= 3 && n[2] > 0 } }),
])

rule('NO_GRADIENT', 1, () => scan(/gradient\(/g, () => 'raw gradient. Use var(--sky-*-gradient) from tokens.css, or ndvi.js for data.', { skip: (r) => ALLOW_RAW.test(r) }))

rule('NO_TRANSITION_ALL', 1, () => scan(/transition:\s*all\b/g, () => 'list the properties instead of "all".'))

rule('RAW_INLINE_ICON', 3, () => scan(/<svg class="svg-icon/g, () => 'pasted raw SVG icon. Use a Phosphor component.', { skip: (r) => r === 'App.vue' }))

// ---- Phase 0: cleanup ----
const DEAD = ['components/AppHeader.vue', 'components/CampaignOutput.vue', 'components/EmptyState.vue',
  'components/HistoryList.vue', 'components/MediaPreview.vue', 'components/ResultsSkeleton.vue',
  'components/ScoreBand.vue', 'views/Onboarding.vue', 'views/Inbox.vue', 'views/Selfie.vue']
rule('DEAD_FILES_REMOVED', 0, () => DEAD.filter(exists).map((f) => `${f} still exists (unused, wrong product branding).`))
rule('ROUTER_NO_DEAD_IMPORTS', 0, () => /Onboarding|Inbox|Selfie/.test(read(path.join(SRC, 'router/index.js')))
  ? ['router/index.js still references Onboarding/Inbox/Selfie.'] : [])
rule('NO_TERRAPULSE', 0, () => files.filter((f) => /terrapulse/i.test(f.text)).map((f) => `${f.rel} mentions Terrapulse.`))

// ---- Phase 1: identity ----
rule('TOKENS_FILE', 1, () => {
  const t = read(path.join(SRC, 'styles/tokens.css')), m = read(path.join(SRC, 'main.js')), h = read(INDEX)
  const out = []
  if (!t.includes('--color-monsoon-sky')) out.push('src/styles/tokens.css missing or not the KrishiSetu token file.')
  if (!t.includes('prefers-reduced-motion')) out.push('tokens.css lacks the prefers-reduced-motion block.')
  if (!t.includes(':lang(bn)')) out.push('tokens.css lacks the Bengali/Hindi leading rules.')
  if (!t.includes('data-risk="storm"')) out.push('tokens.css lacks the data-risk sky states.')
  if (!m.includes('tokens.css')) out.push('main.js must import ./styles/tokens.css first.')
  if (!/switzer/i.test(h)) out.push('index.html does not load Switzer (Fontshare).')
  if (!/Cormorant/.test(h)) out.push('index.html does not load Cormorant Garamond.')
  if (!/Noto\+Serif\+Bengali/.test(h)) out.push('index.html does not load Noto Serif Bengali.')
  if (/Archivo/.test(h)) out.push('index.html still loads Archivo.')
  return out
})
rule('NAV_ICON_HAMBURGER', 1, () => /PhList/.test(read(path.join(SRC, 'App.vue'))) ? ['App.vue: Sathi nav uses a hamburger icon (PhList). Use PhLeaf or PhPlant.'] : [])

// ---- Phase 2: story page + sharing ----
rule('SATHI_ROUTE', 2, () => /path:\s*'\/sathi'/.test(read(path.join(SRC, 'router/index.js'))) ? [] : ["router: '/sathi' route missing; '/' must be the story page."])
rule('OG_TAGS', 2, () => ['og:title', 'og:description', 'og:image', 'twitter:card']
  .filter((t) => !read(INDEX).includes(t)).map((t) => `index.html missing ${t}.`))
rule('HEAVY_LIBS_ISOLATED', 2, () => files.filter((f) => /^(views\/(Home|Admin|DevTool)\.vue|components\/)/.test(f.rel) && f.rel !== 'views/Admin.vue'
  && /from ['"](gsap|d3-geo)/.test(f.text)).map((f) => `${f.rel} imports gsap/d3-geo. Only the story route and Admin may.`))

// ---- Copy rewrites and trust fixes, per portal ----
const COPY = [
  [3, 'views/Admin.vue', ['regional outbreak command center', 'Active trans-boundary outbreak vectors', 'Agro-ecological interstate map', 'Inject simulated outbreak event']],
  [4, 'views/Home.vue', ['observation ledger', 'Specimen Intake', 'Verified diagnostic pathology', 'management dossier', 'Sync Environmental Telemetry']],
  [5, 'views/DevTool.vue', ['cross-state interoperability console', 'Heterogeneous state-specific payload', 'Standardized FarmContext v1.0']],
]
for (const [from, rel, strs] of COPY) rule(`COPY_REWRITE ${rel}`, from, () => {
  const f = files.find((x) => x.rel === rel); if (!f) return [`${rel} not found.`]
  return strs.filter((s) => f.text.toLowerCase().includes(s.toLowerCase())).map((s) => `${rel} still says "${s}". Apply the copy table.`)
})
rule('TRUST_HARDCODED_STATUS', 3, () => {
  const a = read(path.join(SRC, 'views/Admin.vue')), out = []
  if (/>\s*24,580\s*</.test(a)) out.push('Admin.vue: KPI 24,580 is a literal. Bind to data or label it "sample".')
  if (/Malda Hub \(Active Outbreak\)/.test(a)) out.push('Admin.vue: map says Malda is an active outbreak as a literal. Derive from alerts.')
  return out
})
rule('TRUST_HUMIDITY_LABEL', 4, () => /\(Elevated\)/.test(read(path.join(SRC, 'views/Home.vue')))
  ? ['Home.vue: "(Elevated)" is hard-coded. Compute the label from the humidity value vs the 82% threshold.'] : [])

// ---- The sky carries the status ----
const has = (rels, re) => files.filter((f) => rels.some((r) => f.rel === r || f.rel.startsWith(r))).some((f) => re.test(f.text))
rule('STORY_HAS_SKY_HERO', 2, () => has(['views/Story.vue'], /sky-hero/) ? [] : ['views/Story.vue must open with a .sky-hero band.'])
rule('ADMIN_SKY_FOLLOWS_ALERTS', 3, () => has(['views/Admin.vue'], /data-risk/) ? [] : ['views/Admin.vue: sky strip needs :data-risk derived from alerts.'])
rule('SATHI_SKY_FOLLOWS_HUMIDITY', 4, () => has(['views/Home.vue', 'components/sathi/'], /data-risk/) ? [] : ['Home: sky strip needs :data-risk derived from the humidity risk.'])
rule('LANG_ATTRIBUTE', 4, () => files.some((f) => /documentElement\.lang/.test(f.text)) ? [] : ['Set document.documentElement.lang (bn|hi|en) on language change so Indic leading applies.'])
rule('SETU_HAS_SKY_STRIP', 5, () => has(['views/DevTool.vue'], /class="[^"]*\bsky\b/) ? [] : ['views/DevTool.vue must start with a .sky strip.'])

// ---- Size ----
rule('HOME_MAX_600_LINES', 4, () => {
  const n = (files.find((f) => f.rel === 'views/Home.vue')?.text.split('\n').length) || 0
  return n > 600 ? [`views/Home.vue is ${n} lines (max 600). Extract sections into components/sathi/*.vue and shared CSS into src/styles/.`] : []
})
rule('VUE_MAX_700_LINES', 6, () => files.filter((f) => f.rel.endsWith('.vue') && f.text.split('\n').length > 700)
  .map((f) => `${f.rel} is ${f.text.split('\n').length} lines (max 700).`))

// ---- Report (kept short so a small context window can act on it) ----
let errors = 0
for (const r of results) {
  if (!r.hits.length) { console.log(`ok    ${r.id}`); continue }
  errors += r.hits.length
  console.log(`FAIL  ${r.id} (${r.hits.length})`)
  const shown = showAll ? r.hits : r.hits.slice(0, 6)
  shown.forEach((h) => console.log(`        ${h}`))
  if (r.hits.length > shown.length) console.log(`        ... +${r.hits.length - shown.length} more (--all to list)`)
}
console.log(errors ? `\nPHASE ${phase}: ${errors} problem(s). NOT DONE.` : `\nPHASE ${phase}: PASS`)
process.exit(errors ? 1 : 0)
