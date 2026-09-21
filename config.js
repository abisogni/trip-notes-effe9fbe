// Supabase project credentials.
// The "anon / public" key is safe to expose in client-side code —
// access is controlled by Row Level Security policies (see supabase-setup.sql).
// Copenhagen shares the paris-trip-2026 Supabase project (separate tables).
const SUPABASE_URL = "https://sqcdwnsqbqdaxieiiewd.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_96IiulcV3D1b-wZphVBYrw_RkBgsmXE";

// Everything trip-specific lives here so app.js stays generic.
const TRIP = {
  identityKey: "copenhagen_journal_identity",
  pinsTable: "copenhagen_pins",
  commentsTable: "copenhagen_comments",
  realtimeChannel: "copenhagen-live",

  // Home base (placeholder: Rådhuspladsen — replace once the hotel is booked/known).
  hotel: { lat: 55.6761, lng: 12.5683, name: "Hotel (TBD)" },

  // Nominatim viewbox "left,top,right,bottom" (lon/lat) around central Copenhagen,
  // and the suffix appended to typed place names when geocoding.
  geocodeViewbox: "12.45,55.72,12.72,55.62",
  geocodeSuffix: "Copenhagen",

  // Photos upload straight from the browser to Cloudinary (unsigned preset).
  // Fill in once the Cloudinary account/preset exists.
  cloudinary: { cloudName: "", uploadPreset: "", folder: "copenhagen-2026" },
};
