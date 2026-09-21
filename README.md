# Copenhagen Trip Journal (Alex & Jamila, 17-24 Oct 2026)

Cloned from the Paris trip site. A discovery guide with a live map, journal
entries and photos, and a way to add new places while out and about.

## Architecture

- Static site: `index.html` + `app.js` + `config.js` + `skyline.svg`, on GitHub Pages.
- **All trip-specific settings are in `config.js`** (`TRIP`): table names, hotel,
  geocoding area, Cloudinary. `app.js` is generic.
- Trip id: `2026-10-copenhagen` (YYYY-MM of trip start + slug). Used for every DB row and the Cloudinary folder.
- Supabase (shared `paris-trip-2026` project): shared `trip_pins` / `trip_comments`
  tables scoped by `trip_id`. Append-only via RLS.
- Photos: uploaded from the browser to Cloudinary (account alex@alexbisogni.com,
  cloud `ffi8egjg`, unsigned preset `trip-photos`) into `trips/2026-10-copenhagen/`.

## Guide content (`guide.json`)

The fixed guide lives in `guide.json` and is rendered by `guide.js`: trip
title/hero text, sections, pins (each with a permanent `id`), the notes and
conditions boxes, and the reference table (built automatically from the pins,
with distances computed from `trip.anchor`). Change the trip by editing that
file only; `index.html` is a shell.

- **Pin `id`s are permanent.** Journal entries are stored against the pin id
  (per `trip_id`), so never rename or reuse an id once the trip is under way.
  Reordering or adding pins is safe.
- Places added during the trip are NOT in `guide.json`; they live in the
  `trip_pins` table and are drawn under "added by you". Notes and photos on any
  pin live in `trip_comments` / Cloudinary.
- `*word*` in a section title renders as italics.

## Notes

- Short Google Maps links (`maps.app.goo.gl/...`) can't be read in-browser.
  Use the full link or a place name, or `address [Bracket Name]`.
- Public repo with an unguessable name (GitHub Pages free plan). Don't link it publicly.
- Supabase free projects pause after ~1 week idle; restore from the dashboard.
