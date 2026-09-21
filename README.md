# Copenhagen Trip Journal (Alex & Jamila, 17-24 Oct 2026)

Cloned from the Paris trip site. A discovery guide with a live map, journal
entries and photos, and a way to add new places while out and about.

## Architecture

- Static site: `index.html` + `app.js` + `config.js` + `skyline.svg`, on GitHub Pages.
- **All trip-specific settings are in `config.js`** (`TRIP`): table names, hotel,
  geocoding area, Cloudinary. `app.js` is generic.
- Supabase (shared `paris-trip-2026` project): `copenhagen_pins`,
  `copenhagen_comments` (see `supabase-setup.sql`). Append-only via RLS.
- Photos: uploaded from the browser to Cloudinary with an unsigned preset
  (`TRIP.cloudinary.cloudName` / `uploadPreset`).

## Guide content

The 23 pins, quick-reference notes, October conditions and reference table in
`index.html` are the real Copenhagen guide (from the Claude artifact
`claude.ai/artifact/JBNzcPHthXfpLqKgbMiJbS`), anchored at Kongens Nytorv.
Pin markup: `.pin` with `data-pin-id`, `data-pin-name`, `data-lat`, `data-lng`.
Set the real hotel in `config.js` once known (map marker + "reference point").

## Notes

- Short Google Maps links (`maps.app.goo.gl/...`) can't be read in-browser.
  Use the full link or a place name, or `address [Bracket Name]`.
- Public repo with an unguessable name (GitHub Pages free plan). Don't link it publicly.
- Supabase free projects pause after ~1 week idle; restore from the dashboard.
