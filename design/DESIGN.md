# KrishiSetu: Style Reference
> Sky over the paddy: a painted monsoon sky above, a calm white desk below

**Theme:** light. Adapted from the Cora style reference. Same structure and feel, re-hued and re-typed for a farming product used in Bengali, Hindi and English, often outdoors in bright sun.

KrishiSetu looks up before it looks down. The page opens on a full-bleed painting of a monsoon sky over a Bengal delta, and the interface floats on it like white cards laid against a window. Headlines are a light serif that whispers; the product surface is a neutral sans. Colour is disciplined: one sky teal, one deep treeline green for filled actions, one chilli red for urgency. The painting and the type carry the emotion. The new idea on top of Cora: **the sky is the status**. Clear, overcast or storm sky tells a farmer the field's risk before they read a word.

## What stays from Cora, what changes

| Stays | Changes | Why |
|---|---|---|
| Full-bleed painted sky as canvas, text sits directly on it | Subject: cumulus + autumn tree + birds becomes monsoon cumulus + mango tree + paddy + egrets | Same romance, local subject |
| Light serif display, neutral sans UI | Signifier/Switzer have no Bengali or Devanagari. Display: Cormorant Garamond + Noto Serif Bengali/Devanagari. UI: Switzer + Anek Bangla/Devanagari | Bengali and Hindi are first-class here |
| Sky and white sections alternate | Adds three sky states via `data-risk`: clear, watch, storm | Sky carries meaning |
| Pill on every button and tag | Primary fill is canopy `#05261C`, darker than Cora's navy. It inverts to white on storm sky | Cora's navy is 2.3:1 against its sky. Ours is 3.3:1 |
| Tinted, two-direction floating shadows | Tint is deep-monsoon `11,85,104`, same geometry | Cora's shadows are black despite its own rule |
| One accent colour | Berry red becomes chilli `#BF2F1B` | A crop, and 5.77:1 on white |
| Restricted palette | Adds `leaf` and `straw` as DATA INK only (status badges, gauges) | Agronomic status needs green and amber. Chrome stays single-accent |
| 14-18px body | Body 17px, caption 13px, buttons 52px+ | Sunlight, thumbs, low-end phones |
| Muted greys | Stone `#a1a1a1` (2.58:1) becomes `#5F6B59` (5.62:1). Atmosphere-blue outlines (1.7:1 on sky) become haze `#CDE9EF` (3.8:1) | Cora's fail WCAG AA |
| Heading leading 1.02 | Bengali/Hindi headings 1.35, body 1.65 | 1.02 clips matras and shirorekha |

## Tokens: Colours

| Name | Value | Token | Role |
|---|---|---|---|
| Monsoon Sky | `#0E7AA3` | `--color-monsoon-sky` | Clear-sky canvas for hero and header strips, primary nav background |
| Overcast | `#4A7583` | `--color-overcast` | Sky when risk is "watch" |
| Storm | `#15485B` | `--color-storm` | Sky when an outbreak is active; map ground |
| Deep Monsoon | `#0B5568` | `--color-deep-monsoon` | Shadow tint and outlined actions on white |
| Haze | `#CDE9EF` | `--color-haze` | Outlines and secondary borders on sky |
| Canopy | `#05261C` | `--color-canopy` | Primary filled action: the dark treeline |
| Chilli | `#BF2F1B` | `--color-chilli` | The single accent: urgency, outbreak markers, emphasis ink |
| Cloud White | `#FFFFFF` | `--color-cloud-white` | Cards, quiet sections |
| Paddy Mist | `#EAF0E1` | `--color-paddy-mist` | Nested surfaces |
| Fog | `#D3DBC7` | `--color-fog` | Hairlines on white |
| Line Strong | `#7C8977` | `--color-line-strong` | Input borders |
| Stone | `#5F6B59` | `--color-stone` | Muted text |
| Graphite | `#4E5A49` | `--color-graphite` | Secondary text |
| Ink | `#1F2A22` | `--color-ink` | Body text |
| Night Soil | `#141B16` | `--color-night-soil` | Deepest text, sparingly |
| Leaf, Straw, Straw Fill | `#1F6B3A` `#7A5A0C` `#E3B341` | `--color-leaf` `--color-straw` `--color-straw-fill` | DATA INK ONLY: healthy / watch. Never buttons or chrome |

## Tokens: Typography

- **UI: Switzer** (Latin) with Anek Bangla / Anek Devanagari for those scripts. Body 17px/400, buttons 17px/500, nav 15px/500, labels 13px/500. `--font-sans`.
- **Display: Cormorant Garamond** (Latin) with Noto Serif Bengali / Devanagari. 300 at 48px and up, 500 at 24-36px. Headlines and section titles only, 24px and above. Never body, nav, or button labels. `--font-display`. Cormorant runs small for its size, so the scale is about 25% above Cora's.
- **Mono: IBM Plex Mono** for coordinates, granule IDs and schema only. `--font-mono`.

| Role | Size | Weight | Leading (Latin / bn, hi) | Token |
|---|---|---|---|---|
| caption | 13px | 500 | 1.3 / 1.65 | `--text-caption` |
| body-sm | 15px | 400 | 1.5 / 1.65 | `--text-body-sm` |
| body | 17px | 400 | 1.5 / 1.65 | `--text-body` |
| subheading | 24px | 500 serif | 1.2 / 1.35 | `--text-subheading` |
| heading-sm | 36px | 500 serif | 1.15 / 1.35 | `--text-heading-sm` |
| heading | 48px (clamp 36-48) | 300 serif | 1.1 / 1.35 | `--text-heading` |
| display | 76px (clamp 44-76) | 300 serif | 1.05 / 1.35 | `--text-display` |

Font sources (verify each returns 200 once): Switzer from Fontshare (free), Cormorant Garamond, Noto Serif Bengali, Noto Serif Devanagari, Anek Bangla, Anek Devanagari, IBM Plex Mono from Google Fonts.

## Tokens: Spacing, Shape, Shadow

Spacing 4, 8, 12, 16, 20, 24, 32, 38, 48, 64, 108. Page max-width 1200, section gap 64, card padding 24, element gap 12. Radius: buttons and tags 9999, cards 12, inputs 8, modals 20.

| Name | Value | Token |
|---|---|---|
| card | `0 4px 4px 0 rgba(11,85,104,.12)` | `--shadow-card` |
| float | `4px 6px 8px -2px rgba(11,85,104,.25), -4px -1px 8px -2px rgba(11,85,104,.2)` | `--shadow-float` |
| lift | `4px 6px 8px 0 rgba(11,85,104,.25), -4px -6px 8px 0 rgba(11,85,104,.25)` | `--shadow-lift` |

## Surfaces

| Level | Name | Value | Purpose |
|---|---|---|---|
| 0 | Sky | clear `#0E7AA3`, watch `#4A7583`, storm `#15485B` (gradients in `tokens.css`) | Hero, header strips, share cards. Set with `data-risk` |
| 1 | Cloud White | `#FFFFFF` | Cards and quiet sections |
| 2 | Paddy Mist | `#EAF0E1` | Nested rows and secondary surfaces |

## Components

**Hero Sky Panel.** Full-viewport painting (or its gradient fallback), centered. White serif display at 300, white 17-18px sans below. Text sits directly on the sky, no card, no scrim. Headline zone is kept calm in the painting (see `painting-prompt.md`).

**Header Sky Strip.** The app version of the hero: a 200-260px sky band holding nav, page title (serif 36-48px) and one sentence of state. White cards overlap its lower edge by 48px (`.desk`). "Painting above, calm desk below."

**Primary Filled Action.** Pill, canopy fill, white 17px/500 text, 52px tall (`.btn-xl` 60px for camera and voice). No border. Trailing arrow allowed on the hero CTA only. On storm sky the fill inverts to white with canopy text.

**Secondary Outlined Action.** Pill, 1.5px border. On white: deep-monsoon border and text. On sky: haze border, white text.

**Top Nav.** Solid monsoon-sky bar on app routes, transparent over the hero on the story page. Logo badge left (sprout icon plus wordmark, 1px white border). Links in white 15px/500, active link gets a haze outline pill. Online/offline switch is a small pill.

**Result Card** (Cora's testimonial). White, 12px radius, 24px padding, `--shadow-card`. Diagnosis name in serif 500, one-line action in sans, confidence as plain text. Floats in a row with 24px gaps.

**Field Data Card.** White, `--shadow-card`. Value large in sans 600, label in caption. Status is a pill tag in leaf, straw or chilli. Never colour alone: the pill always carries a word.

**Diagnosis Row** (Cora's email row). Paddy-mist, 8px radius, 12px padding, hairline bottom. Title 17px/500, detail 15px in graphite.

**Sky Status Line.** One sentence under the page title on the sky strip, sentence case, white. Example: "Humidity is high. Check the lower leaves today."

**Map Card.** White card with float shadow holding a storm-coloured map ground. Districts on the NDVI ramp, outbreak in chilli, borders in haze.

**Share Card.** 1080x1350. Sky background (by risk), a white float card with a serif headline in the farmer's language, district, risk, next step, small URL.

## Do's and Don'ts

### Do
- Use the painting (or its gradient) full-bleed for hero and header strips. Never crop it into a banner or place it inside a card.
- Tint every shadow with deep-monsoon and use only the three shadow tokens.
- Pair serif at 300-500 with sans at 400-500. Serif only at 24px and above.
- Use pills for every button and tag.
- Alternate sky and white sections.
- Let the sky state follow the data: clear, watch, storm.
- Keep the filled action darker than the sky it sits on.
- Set `document.documentElement.lang` to bn, hi or en so the taller Indic leading applies.

### Don't
- Don't add hues beyond the palette. Green appears only as the canopy pill, `--color-leaf` on status, and inside the painting.
- Don't use `--color-leaf`, `--color-straw` or `--color-chilli` as button fills or backgrounds.
- Don't put chilli text on sky. It is text-safe on white only.
- Don't use text at reduced opacity on sky. Use white.
- Don't use stone or graphite below 13px, or on paddy-mist below 15px.
- Don't apply blur, glass, glow, gradient overlays or scrims to the sky.
- Don't use body text below 15px. Nothing below 12px anywhere.
- Don't use serif for buttons, nav, body, or Bengali/Hindi text below 24px.
- Don't set leading below 1.3 on any element that can hold Bengali or Hindi.
- Don't use stock farmer photography. The painting is the emotional carrier.

## Imagery

A romantic plein-air oil painting, same spirit as Cora's, translated to the Bengal delta in monsoon: volumetric cumulus over teal sky, a large mango tree on the left edge (Malda's crop), palms and a tin-roofed house at the horizon, layered paddy in flat bands, a river with a small bamboo footbridge far away (the "setu"), a few egrets in flight. Three variants of the same composition drive the sky state: clear, watch (heavy cloud, flat light), storm (dark cloud, egrets low). No people, no text. Icons are Phosphor regular weight, used only where they carry function: camera, microphone, and one arrow on the hero CTA. Brief and generator prompt: `painting-prompt.md`.

## Layout

Rhythm: sky hero, white cards row, sky section, white content, sky CTA. Copy blocks max 1200px centered; the sky is always full-bleed. Inside app routes: sky strip (nav, title, status line), then a `.desk` of white cards overlapping the strip.

Per portal:
- **Kisan Sathi** (`/sathi`): clear-to-watch sky by humidity risk. First card is "Check a leaf" with 60px camera and voice buttons.
- **Kisan Setu** (`/interop`): clear sky. Two cards: state registry data left, standard FarmContext right.
- **Kisan Rakshak** (`/command`): sky follows outbreaks: storm if any active, watch if warnings, clear otherwise.

## Agent Prompt Guide

**Quick reference**
- Sky: `#0E7AA3` clear, `#4A7583` watch, `#15485B` storm (set `data-risk`)
- Quiet section: `#FFFFFF`. Nested: `#EAF0E1`
- Text: `#1F2A22`. Secondary `#4E5A49`. Muted `#5F6B59`
- Primary action: `#05261C` fill, white text (white fill on storm)
- Accent: `#BF2F1B`, on white only
- Shadow tint: `rgb(11,85,104)`

**Example prompts**
1. *Hero:* Full-viewport sky painting (gradient fallback until the image exists). Centered white serif display at 300, one line in Bengali and one in English. White 18px sans below. Canopy pill "Check a leaf" and a haze outline pill "See outbreaks".
2. *Result card on white:* White, 12px radius, 24px padding, `--shadow-card`. Title in serif 500 at 28px, action sentence in sans 17px ink, "Confidence 82%" caption in stone, "High risk" pill in chilli on chilli-wash.
3. *Header strip:* 240px sky band, `data-risk` from humidity. Nav on top, serif 40px farmer name, one status sentence. First white card overlaps it by 48px.
4. *Diagnosis row:* Paddy-mist, 8px radius, 12px padding. Title 17px/500, detail 15px graphite, status pill on the right.

## Quick start

`tokens.css` (import first in `main.js`), `tokens.json` (W3C tokens), `ndvi.js` (the only place raw NDVI colours live). Tailwind is not used in this repo, so Cora's `theme.css` and `variables.css` are replaced by `tokens.css`.
