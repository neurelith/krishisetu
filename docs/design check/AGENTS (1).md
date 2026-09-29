# KrishiSetu frontend: agent rules (read every session)

You are the hands. The design decisions are already made and live in `frontend/src/styles/tokens.css`,
`frontend/src/styles/ndvi.js`, and the phase you are given. Do not invent new ones.

1. Do only the phase I give you. Touch only the files that phase lists. If another file needs a change, stop and ask.
2. One file at a time. Never rewrite a file over 300 lines in one go. Edit sections. Never delete a file unless the phase lists it.
3. Colours: only `var(--token)`. No hex, rgb() or named colours anywhere except `styles/tokens.css` and `styles/ndvi.js`.
4. No gradients (except `NDVI_GRADIENT`), no blur, no glow, no drop shadows, no `transition: all`.
5. Smallest text is 12px. Body is 17px (`var(--step-0)`). Buttons and inputs are at least 48px tall, primary actions 56px.
6. Icons: Phosphor components only. Never paste raw `<svg>` path icons.
7. Copy: use the wording in the phase prompt exactly. Plain verbs, sentence case. Every string that is already localised needs `bn`, `hi` and `en`.
8. Never invent data. If a number or status is not in the API response or the sample data, bind it to real data or label it "sample". Never hard-code a status word like "Elevated".
9. Do not touch `backend/`, `api.js`, or the composables. Do not add dependencies unless the phase names them.
10. Do not add comments that narrate what you did.

## Definition of done (no exceptions)

Run both, from `frontend/`:

    npm run check -- --phase N
    npm run build

You may say "done" only if the first prints `PHASE N: PASS` and the second succeeds.
Paste both outputs in your reply. If either fails, fix it and run again. Do not argue with the checker, and do not edit
`scripts/design-check.mjs` or `tokens.css` to make it pass.

Then run the app and take screenshots of every changed route at 1440px and 390px wide. Stop and wait for review.
