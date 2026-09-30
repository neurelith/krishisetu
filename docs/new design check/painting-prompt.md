# Hero painting: brief and generator prompt

Make three images from one composition (same seed or img2img), one per sky state. Same scene, different weather.

## Prompt (clear)

Romantic plein-air oil painting, wide landscape, 19th-century atmospheric style (Hudson River School light) translated to the Bengal delta in monsoon season. Vivid teal-cerulean sky filling the upper 60% with volumetric white cumulus clouds and warm light breaking through. A large mango tree with deep green foliage at the far left edge. A distant line of coconut and betel palms and one tin-roofed farmhouse at the horizon. Flat layered bands of green paddy fields below in three tones. A narrow river reflecting the sky with a small bamboo footbridge far in the distance. Four or five white egrets in flight, upper right. Soft visible brushwork, natural, calm, luminous. Composition: horizon at 62% of the height. The upper-centre area, 40% wide by 30% tall, stays calm mid-blue sky with no bright cloud, so white headline text is readable there. Dominant sky colour close to #0E7AA3.

## Variants

- **Watch:** same scene under heavy grey-teal cloud, flat diffuse light, no sun, egrets lower. Sky close to #4A7583.
- **Storm:** same scene under dark slate-teal thunderheads, wind pushing the palms and paddy, egrets near the ground, faint rain on the far horizon. Sky close to #15485B.

## Negative

Text, signature, watermark, people, vehicles, power lines, cartoon, flat vector, 3D render, HDR, neon, purple, pink sunset, lens flare.

## Exports (per variant)

| File | Size | Use |
|---|---|---|
| `hero-{state}-2400.avif` / `.webp` | 2400x1350 | Desktop hero |
| `hero-{state}-1080.avif` / `.webp` | 1080x1920 (portrait crop) | Mobile hero and share-card sky |
| `og-{state}.jpg` | 1200x630 | Open Graph |

Targets: desktop AVIF 150 KB or less, mobile AVIF 90 KB or less. Serve with `srcset`. Only the current state's image loads. App routes use the CSS gradients in `tokens.css`, not the painting. The gradient shows instantly while the image loads, so LCP is never blocked.

## Check before accepting

1. White text at 40px on the headline zone reads clearly at arm's length on a phone in daylight.
2. No cloud brighter than the sky colour behind the headline zone.
3. The three variants are the same scene, so switching state feels like weather changing, not a different page.
