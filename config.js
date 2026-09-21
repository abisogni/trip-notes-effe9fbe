// Supabase project credentials.
// The "anon / public" key is safe to expose in client-side code —
// access is controlled by Row Level Security policies (see supabase-setup.sql).
// Shared Supabase project (paris-trip-2026) with shared trip_* tables, scoped by trip_id.
const SUPABASE_URL = "https://sqcdwnsqbqdaxieiiewd.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_96IiulcV3D1b-wZphVBYrw_RkBgsmXE";

// Everything trip-specific lives here so app.js stays generic.
const TRIP = {
  // Trip id = YYYY-MM-slug of the trip start. It scopes every database row
  // and names the Cloudinary folder (trips/<id>/).
  id: "2026-10-copenhagen",
  identityKey: "2026-10-copenhagen_journal_identity",
  pinsTable: "trip_pins",
  commentsTable: "trip_comments",
  realtimeChannel: "2026-10-copenhagen-live",

  // Map anchor = Kongens Nytorv (the guide's reference point). Swap for the real hotel once known.
  hotel: { lat: 55.6806, lng: 12.5859, name: "Kongens Nytorv (anchor — hotel TBD)" },

  // Nominatim viewbox "left,top,right,bottom" (lon/lat) around central Copenhagen,
  // and the suffix appended to typed place names when geocoding.
  geocodeViewbox: "12.45,55.72,12.72,55.62",
  geocodeSuffix: "Copenhagen",

  // Photos upload straight from the browser to Cloudinary (unsigned preset).
  // Account: alex@alexbisogni.com. Preset "trip-photos" is unsigned (no secret in the page).
  cloudinary: { cloudName: "ffi8egjg", uploadPreset: "trip-photos", folder: "trips/2026-10-copenhagen" },
};
