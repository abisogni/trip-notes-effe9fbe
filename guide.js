// Renders guide.json (the fixed guide content) into the page shell.
// User-added places/notes/photos are NOT here — they live in Supabase (see app.js).

const GUIDE = { data: null };

function gEsc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
// *word* -> <em>word</em> (after escaping, so JSON stays text-only)
function gEm(s) { return gEsc(s).replace(/\*(.+?)\*/g, "<em>$1</em>"); }

// Scatter slots for the fixed corkboard layer (viewport %, rotation deg).
// Fixed positioning means these stay put as the page scrolls behind it —
// a wallpaper, not tied to page length. Cycles if there are more photos.
const CORK_SLOTS = [
  { top: 6, left: 4, w: 15, rot: -7 },
  { top: 62, left: 2, w: 13, rot: 5 },
  { top: 14, left: 84, w: 15, rot: 6 },
  { top: 70, left: 85, w: 14, rot: -5 },
  { top: 38, left: 92, w: 11, rot: 8 },
  { top: 88, left: 12, w: 12, rot: -4 },
  { top: 40, left: -2, w: 12, rot: 4 },
  { top: 4, left: 40, w: 10, rot: -6 },
];

function renderCorkboard(photos) {
  const board = document.getElementById("corkboard");
  if (!photos || !photos.length) return;
  board.innerHTML = photos
    .map((p, i) => {
      const s = CORK_SLOTS[i % CORK_SLOTS.length];
      return `<div class="cork-photo" style="top:${s.top}%;left:${s.left}%;width:${s.w}vw;transform:rotate(${s.rot}deg);">
        <span class="cork-pin"></span><img src="${gEsc(p.src)}" alt="">
      </div>`;
    })
    .join("");
}

function gDistKm(a, lat, lng) {
  const R = 6371, rad = (d) => (d * Math.PI) / 180;
  const dp = rad(lat - a.lat), dl = rad(lng - a.lng);
  const x = Math.sin(dp / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(lat)) * Math.sin(dl / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(x));
}
function gWalk(km) {
  const m = Math.round(km * 12);
  return km < 1.6 ? `${m} min walk` : `~${m} min walk — or bike / metro`;
}

function gPinHtml(p, num, anchor) {
  const km = gDistKm(anchor, p.lat, p.lng);
  const q = encodeURIComponent(p.name.split(" (")[0] + " " + TRIP.geocodeSuffix).replace(/%20/g, "+");
  const notes = (p.notes || []).map((n) => `<div class="pin-note"><strong>${gEsc(n.label)}</strong>${gEsc(n.text)}</div>`).join("");
  const egg = p.easter_egg ? `<div class="egg"><strong>Easter egg</strong>${gEsc(p.easter_egg)}</div>` : "";
  const tags = (p.tags || []).map((t) => `<span class="tag t-${gEsc(t.color)}">${gEsc(t.text)}</span>`).join("");
  return `
<div class="pin" data-pin-id="${gEsc(p.id)}" data-pin-name="${gEsc(p.name)}" data-lat="${p.lat}" data-lng="${p.lng}">
  <div class="pin-left"><div class="pin-num c-${gEsc(p.color)}">${num}</div><div class="pin-vline"></div></div>
  <div class="pin-right">
    <div class="pin-name">${gEsc(p.name)}</div>
    <div class="pin-coords">
      ${gEsc(p.area)} &nbsp;·&nbsp; ${p.lat.toFixed(4)}°N, ${p.lng.toFixed(4)}°E &nbsp;·&nbsp;
      <a href="https://maps.apple.com/?q=${q}&ll=${p.lat},${p.lng}">Apple Maps</a> &nbsp;·&nbsp;
      <a href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lng}">Google Maps</a>
    </div>
    <div class="pin-meta-row"><span class="pin-dist">${km.toFixed(2)} km from ${gEsc(anchor.name)} — ${gWalk(km)}</span></div>
    <p class="pin-desc">${gEsc(p.description)}</p>
    ${notes}${egg}
    <div class="pin-tags">${tags}</div>
  </div>
</div>`;
}

function renderGuide(g) {
  const t = g.trip, anchor = t.anchor;
  document.title = t.page_title;
  renderCorkboard(t.background_photos);

  document.getElementById("hero").innerHTML = `
  <div class="eyebrow">${gEsc(t.eyebrow)}</div>
  <h1>${gEsc(t.heading[0])}<br><em>${gEsc(t.heading[1])}</em></h1>
  <p class="hero-sub">${gEsc(t.subtitle)}</p>
  <div class="hero-meta">${t.hero_meta.map((m) => `<div class="meta-item"><strong>${gEsc(m.label)}</strong>${gEsc(m.text)}</div>`).join("")}</div>`;

  document.getElementById("skyline-top").setAttribute("aria-label", t.skyline_alt);
  document.getElementById("ref-box").innerHTML = t.ref_bar
    .map((r) => `<span>${r.label ? `<strong>${gEsc(r.label)}</strong> ` : ""}${gEsc(r.text)}</span>`).join("");
  document.getElementById("live-label").textContent = t.live_label;
  document.getElementById("added-label").textContent = t.added_label;

  let n = 0, rows = "", pins = "";
  g.sections.forEach((s) => {
    pins += `<div class="section-head"><div class="section-label">${gEsc(s.label)}</div><h2 class="section-title">${gEm(s.title)}</h2></div>`;
    s.pins.forEach((p) => {
      n += 1;
      pins += gPinHtml(p, n, anchor);
      rows += `<tr><td>${n}</td><td>${gEsc(p.name)}</td><td>${gEsc(p.area.split(" · ")[0])}</td><td>${p.lat.toFixed(4)}, ${p.lng.toFixed(4)}</td><td>${gDistKm(anchor, p.lat, p.lng).toFixed(2)} km</td></tr>`;
    });
  });
  document.getElementById("guide-pins").innerHTML = pins;

  const notes = g.notes.items.map((i) => `<strong>${gEsc(i.label)}</strong> ${gEsc(i.text)}`).join("<br><br>");
  const prac = g.practical.items.map((i) => `<div class="prac-item"><span>${gEsc(i.label)}</span>${gEsc(i.text)}</div>`).join("");
  document.getElementById("guide-info").innerHTML = `
<div class="food-card" style="margin-top:40px;"><div class="food-head">${gEsc(g.notes.title)}</div>${notes}</div>
<div class="practical"><h3>${gEsc(g.practical.title)}</h3><div class="prac-grid">${prac}</div></div>
<div class="ref-table-section"><h3>Quick reference</h3><div class="table-scroll"><table>
  <thead><tr><th>#</th><th>Location</th><th>Area</th><th>GPS</th><th>Dist.</th></tr></thead><tbody>${rows}</tbody></table></div>
  <p style="font-size:11px;color:var(--muted);margin-top:10px;">${gEsc(t.table_footnote)}</p></div>`;

  const cl = (t.background_photos || []).map((p) => {
    const c = p.credit;
    return `<a href="${gEsc(c.page)}" target="_blank" rel="noopener">${gEsc(c.title)}</a> by ${gEsc(c.author)}, <a href="${gEsc(c.license_url)}" target="_blank" rel="noopener">${gEsc(c.license)}</a>`;
  });
  document.getElementById("credits").innerHTML = cl.length
    ? `<strong>Background photo credits.</strong> ${cl.join(" &nbsp;·&nbsp; ")}.${t.credits_note ? " " + gEsc(t.credits_note) : ""}`
    : "";
}

async function loadGuide() {
  const res = await fetch("guide.json?v=" + (window.GUIDE_VERSION || "1"), { cache: "no-cache" });
  if (!res.ok) throw new Error("guide.json " + res.status);
  GUIDE.data = await res.json();
  renderGuide(GUIDE.data);
}
