// The ONLY place gradients and raw hex are allowed outside tokens.css.
// Sentinel-2 NDVI ramp: bare soil -> straw -> young paddy -> dense canopy.
export const NDVI_STOPS = ['#7A4A2B', '#D9B54A', '#6BBF3B', '#0B7A4B']
export const NDVI_GRADIENT = `linear-gradient(90deg, ${NDVI_STOPS.join(', ')})`
export function ndviColor(v) {
  const t = Math.max(0, Math.min(1, v)), i = Math.min(2, Math.floor(t * 3)), f = t * 3 - i
  const p = (h) => [1, 3, 5].map((k) => parseInt(h.slice(k, k + 2), 16))
  const a = p(NDVI_STOPS[i]), b = p(NDVI_STOPS[i + 1])
  return `rgb(${a.map((c, k) => Math.round(c + (b[k] - c) * f)).join(',')})`
}
