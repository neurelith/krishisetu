# KrishiSetu frontend: agent rules (read every session)

You are the hands. Design decisions are made. Source of truth: `design/DESIGN.md`, `frontend/src/styles/tokens.css`,
`frontend/src/styles/ndvi.js`, plus the phase you are given. Read DESIGN.md before styling anything. Do not invent new decisions.

1. Do only the phase I give you. Touch only the files it lists. If another file needs a change, stop and ask.
2. One file at a time. Never rewrite a file over 300 lines in one go; edit sections. Never delete a file unless the phase lists it.
3. Colours: only `var(--color-*)`, `var(--art-*)` or the legacy aliases already in tokens.css. No hex, rgb() or named colours outside `styles/tokens.css` and `styles/ndvi.js`.
4. Shadows: only `var(--shadow-card)`, `var(--shadow-float)`, `var(--shadow-lift)`. Gradients: only `var(--sky-*-gradient)` (and `ndvi.js` for data). Never blur, backdrop-filter, glass, glow, text-shadow, or a scrim over the sky. Never `transition: all`.
5. Palette discipline: chilli is the only accent. `--color-leaf` and `--color-straw` are status ink (tags, gauges), never button fills or backgrounds. Chilli text goes on white only. Text on sky is solid white, never reduced opacity.
6. Type: `var(--font-display)` (serif) only on h1, h2 and `.display`, at 24px and above. Everything else `var(--font-sans)`. Body 17px. Smallest text 13px (hard floor 12px). Never set line-height under 1.3 on anything that can hold Bengali or Hindi.
7. Every button and tag is a pill. Primary action is `.btn-gov-primary` (canopy). Touch targets 52px or more; camera and voice use `.btn-xl`.
8. Sky: header bands are `.sky` with `:data-risk="clear|watch|storm"` computed from real data, never hard-coded.
9. Icons: Phosphor components only. No pasted raw `<svg>` icons.
10. Copy: use the phase wording exactly. Sentence case, plain verbs. Every string already localised needs `bn`, `hi` and `en`.
11. Never invent data. If a number or status is not in the API response or sample data, bind it to real data or label it "Sample data". Never hard-code a status word like "Elevated".
12. Do not touch `backend/`, `api.js`, or the composables. No new dependencies unless the phase names them. Do not create or download images.
13. No comments that narrate what you did.

## Definition of done (no exceptions)

Run both, from `frontend/`:

    npm run check -- --phase N
    npm run build

You may say "done" only if the first prints `PHASE N: PASS` and the second succeeds. Paste both outputs in your reply.
If either fails, fix it and run again. Do not argue with the checker. Do not edit `scripts/design-check.mjs` or `tokens.css` to make it pass.

Then run the app and take screenshots of every changed route at 1440px and 390px wide. Stop and wait for review.
