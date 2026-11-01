// Shared drawing code for the Poetics social editors (social post, video thumbnail).
// The look is brand-kit/design-system.md: paper and ink, Instrument Serif for display, Inter Tight
// for text, photographs in apertures, hairlines, the wordmark. No gradients, no glows, no italics.
// build-social-editors.py inlines this file, the fonts and the wordmark into each editor.html.

const THEMES = {
  light: { paper: '#EFF0EC', deep: '#E5E8E3', shade: '#C5CBC4', ink: '#121614', soft: '#5B625C', lens: '#16249C' },
  dark:  { paper: '#121614', deep: '#1C211E', shade: '#3A423D', ink: '#F4F5F3', soft: '#8A918B', lens: '#8F9CFF' },
};
const DISPLAY = "'Instrument Serif', Georgia, serif";
const SANS = "'Inter Tight', 'Helvetica Neue', Arial, sans-serif";

// The wordmark, recoloured per theme (an SVG drawn as an image).
const wordmarks = {};
function wordmark(color) {
  if (!wordmarks[color]) {
    const img = new Image();
    img.src = 'data:image/svg+xml;base64,' + btoa(WORDMARK_SVG.replace('fill="#121614"', `fill="${color}"`));
    img.onload = () => window.render && window.render();
    wordmarks[color] = img;
  }
  return wordmarks[color];
}
function drawWordmark(ctx, color, x, y, h) {
  const img = wordmark(color);
  if (img.complete && img.naturalWidth) ctx.drawImage(img, x, y, h * 148 / 20, h);
}

// The wordmark's O, outer edge, as a 2px outline: decoration, used once (the closing band).
function drawRing(ctx, color, x, y, h) {
  const s = h / 20, ox = x - 20.068 * s;
  const P = (a, b) => [ox + a * s, y + b * s];
  ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.beginPath();
  ctx.moveTo(...P(30.102, 0)); ctx.lineTo(...P(46.825, 0));
  ctx.bezierCurveTo(...P(52.366, 0), ...P(56.859, 4.477), ...P(56.859, 10));
  ctx.bezierCurveTo(...P(56.859, 15.523), ...P(52.366, 20), ...P(46.825, 20));
  ctx.lineTo(...P(30.102, 20));
  ctx.bezierCurveTo(...P(24.56, 20), ...P(20.068, 15.523), ...P(20.068, 10));
  ctx.bezierCurveTo(...P(20.068, 4.477), ...P(24.56, 0), ...P(30.102, 0));
  ctx.stroke(); ctx.restore();
}

function roundRect(ctx, x, y, w, h, r) {
  const [tl, tr, br, bl] = Array.isArray(r) ? r : [r, r, r, r];
  ctx.beginPath();
  ctx.moveTo(x + tl, y); ctx.lineTo(x + w - tr, y); ctx.arcTo(x + w, y, x + w, y + tr, tr);
  ctx.lineTo(x + w, y + h - br); ctx.arcTo(x + w, y + h, x + w - br, y + h, br);
  ctx.lineTo(x + bl, y + h); ctx.arcTo(x, y + h, x, y + h - bl, bl);
  ctx.lineTo(x, y + tl); ctx.arcTo(x, y, x + tl, y, tl); ctx.closePath();
}

// A photograph in an aperture: cover-fit, cropped around the focal point. Empty -> a paper-deep frame.
const FOCAL = { center: [0.5, 0.5], top: [0.5, 0], bottom: [0.5, 1], left: [0, 0.5], right: [1, 0.5] };
function drawAperture(ctx, t, img, x, y, w, h, r, focal) {
  ctx.save(); roundRect(ctx, x, y, w, h, r); ctx.clip();
  ctx.fillStyle = t.deep; ctx.fillRect(x, y, w, h);
  if (img && img.naturalWidth) {
    const s = Math.max(w / img.naturalWidth, h / img.naturalHeight);
    const dw = img.naturalWidth * s, dh = img.naturalHeight * s;
    const [fx, fy] = FOCAL[focal] || FOCAL.center;
    ctx.drawImage(img, x - (dw - w) * fx, y - (dh - h) * fy, dw, dh);
  }
  ctx.restore();
}

// Greedy word wrap. Returns the lines.
function wrapLines(ctx, text, maxW) {
  const out = [];
  for (const para of String(text || '').split('\n')) {
    let line = '';
    for (const word of para.split(/\s+/).filter(Boolean)) {
      const test = line ? line + ' ' + word : word;
      if (ctx.measureText(test).width > maxW && line) { out.push(line); line = word; } else line = test;
    }
    out.push(line);
  }
  return out;
}

// The largest size from `sizes` at which the text fits in maxLines. Sets ctx.font.
function fit(ctx, text, family, weight, sizes, maxW, maxLines) {
  for (const size of sizes) {
    ctx.font = `${weight} ${size}px ${family}`;
    const lines = wrapLines(ctx, text, maxW);
    if (lines.length <= maxLines) return { size, lines };
  }
  const size = sizes[sizes.length - 1];
  ctx.font = `${weight} ${size}px ${family}`;
  return { size, lines: wrapLines(ctx, text, maxW).slice(0, maxLines), clipped: true };
}

// Draw lines with their first baseline at y. Returns the y below the last line.
function drawLines(ctx, lines, x, y, size, lh, color) {
  ctx.fillStyle = color; ctx.textBaseline = 'alphabetic';
  lines.forEach((l, i) => ctx.fillText(l, x, y + size * 0.82 + i * size * lh));
  return y + lines.length * size * lh;
}

function hairline(ctx, color, x, y, w) { ctx.fillStyle = color; ctx.fillRect(x, y, w, 2); }

// The copy check: the same rules as decks (guides/anti-slop.md), live in the editor.
const SLOP = ['journey', 'seamless', 'unforgettable', 'magical', 'magic', 'cutting-edge', 'revolutionary',
  'revolutionize', 'solution', 'leverage', 'unlock', 'next-generation', 'elevate', 'game-changing', 'delve',
  'empower', 'world-class', 'bespoke', 'hassle-free', 'step into', 'like never before', 'redefin',
  'reimagin', 'the future of', 'immerse yourself', 'dive into', 'ready when you are', "let's", 'shall we',
  'breathtaking', 'beyond imagination'];
function copyCheck(fields) {
  const issues = [];
  for (const [name, text] of Object.entries(fields)) {
    if (!text) continue;
    const low = text.toLowerCase();
    if (text.includes('—')) issues.push(`${name}: an em dash. Use a colon, comma or full stop.`);
    if (text.includes('!')) issues.push(`${name}: an exclamation mark.`);
    if (/\*[^*]+\*/.test(text)) issues.push(`${name}: *asterisks* (there are no italics). Remove them.`);
    if (/\b[A-Z]{4,}\b/.test(text.replace(/\b(VR|AR|XR|TIF|LBVR)\b/g, ''))) issues.push(`${name}: capitals. Use sentence case.`);
    if (/[\u{1F300}-\u{1FAFF}☀-➿]/u.test(text)) issues.push(`${name}: an emoji.`);
    const hit = SLOP.find(w => low.includes(w));
    if (hit) issues.push(`${name}: "${hit}" reads as stock copy. Say the plain fact.`);
  }
  return issues;
}

// Fonts: loaded from the embedded data, then the preview renders.
function loadFonts(faces) {
  return Promise.all(faces.map(([family, weight, url, range]) =>
    new FontFace(family, `url(${url})`, { weight: String(weight), unicodeRange: range }).load()
      .then(f => document.fonts.add(f)).catch(() => {})));
}

// The photo input: a local file, never uploaded.
function bindPhoto(inputId, onload) {
  const input = document.getElementById(inputId);
  const img = new Image();
  img.onload = () => onload(img);
  input.addEventListener('change', () => {
    const f = input.files && input.files[0];
    if (f) img.src = URL.createObjectURL(f);
  });
  return img;
}

function exportPNG(canvas, name) {
  const a = document.createElement('a');
  a.download = name;
  a.href = canvas.toDataURL('image/png');
  a.click();
}
