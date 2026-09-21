#!/usr/bin/env python3
"""Archive a trip: pins added during the trip, journal entries and photos.

  python3 tools/export_trip.py --out "<folder>" [--trip-id 2026-10-copenhagen] [--to-cloudinary]

Reads Supabase + Cloudinary settings from config.js (public read access only,
no secrets needed). Writes into --out:
  pins.json        places added during the trip (trip_pins)
  comments.json    journal entries (trip_comments) + local photo path
  photos/          every photo, downloaded
  summary.md       human-readable journal grouped by place (Obsidian-friendly)
  guide.json       copy of the repo's guide.json, if present
--to-cloudinary also uploads each photo to trips/<trip-id>/ using the unsigned
preset and records the new URL in comments.json (the live site is not changed).
"""
import argparse, json, os, re, shutil, subprocess, sys, urllib.parse

def curl(url, headers=(), dest=None):
    """HTTP GET via curl (macOS system Python often lacks CA certs)."""
    cmd = ["curl", "-sSfL", "--max-time", "90"] + [x for h in headers for x in ("-H", h)] + (["-o", dest] if dest else []) + [url]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode: sys.exit(f"GET failed ({r.returncode}): {url}\n{r.stderr.decode()[:300]}")
    return r.stdout
from collections import OrderedDict

def cfg(path):
    t = open(path, encoding="utf-8").read()
    g = lambda pat: (re.search(pat, t) or [None, ""])[1]
    return {"url": g(r'SUPABASE_URL\s*=\s*"([^"]+)"'), "key": g(r'SUPABASE_ANON_KEY\s*=\s*"([^"]+)"'),
            "id": g(r'\bid:\s*"([^"]+)"'), "cloud": g(r'cloudName:\s*"([^"]*)"'), "preset": g(r'uploadPreset:\s*"([^"]*)"')}

def fetch(c, table, trip_id):
    rows, off = [], 0
    while True:
        u = f'{c["url"]}/rest/v1/{table}?trip_id=eq.{urllib.parse.quote(trip_id)}&order=created_at.asc&select=*&limit=1000&offset={off}'
        chunk = json.loads(curl(u, [f'apikey: {c["key"]}']))
        rows += chunk
        if len(chunk) < 1000: return rows
        off += 1000

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True); ap.add_argument("--trip-id"); ap.add_argument("--config", default="config.js")
    ap.add_argument("--to-cloudinary", action="store_true")
    a = ap.parse_args()
    c = cfg(a.config); trip = a.trip_id or c["id"]
    if not re.fullmatch(r"\d{4}-\d{2}-[a-z0-9-]+", trip): sys.exit(f"bad trip id: {trip!r}")
    os.makedirs(os.path.join(a.out, "photos"), exist_ok=True)
    pins, comments = fetch(c, "trip_pins", trip), fetch(c, "trip_comments", trip)
    print(f"{trip}: {len(pins)} added pins, {len(comments)} journal entries")
    for i, cm in enumerate(comments, 1):
        if not cm.get("photo_url"): continue
        ext = os.path.splitext(urllib.parse.urlparse(cm["photo_url"]).path)[1] or ".jpg"
        rel = f'photos/{cm["created_at"][:19].replace(":", "").replace("-", "")}_{cm["id"][:8]}{ext}'
        dest = os.path.join(a.out, rel)
        if not os.path.exists(dest):
            curl(cm["photo_url"], dest=dest)
        cm["local_photo"] = rel
        if a.to_cloudinary:
            if not (c["cloud"] and c["preset"]): sys.exit("Cloudinary settings missing in config.js")
            out = subprocess.run(["curl", "-s", "-X", "POST", f'https://api.cloudinary.com/v1_1/{c["cloud"]}/image/upload',
                                  "-F", f"file=@{dest}", "-F", f'upload_preset={c["preset"]}', "-F", f"folder=trips/{trip}"],
                                 capture_output=True, text=True).stdout
            j = json.loads(out)
            if "secure_url" not in j: sys.exit(f"upload failed for {rel}: {out[:200]}")
            cm["cloudinary_url"] = j["secure_url"]; cm["cloudinary_public_id"] = j["public_id"]
        print(f"  photo {i}/{len(comments)} ok", end="\r")
    json.dump(pins, open(os.path.join(a.out, "pins.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(comments, open(os.path.join(a.out, "comments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    if os.path.exists("guide.json"):  # only archive the guide if it belongs to this trip
        if json.load(open("guide.json", encoding="utf-8")).get("trip", {}).get("id") == trip:
            shutil.copy("guide.json", os.path.join(a.out, "guide.json"))
    by = OrderedDict()
    for cm in comments: by.setdefault(cm["pin_name"], []).append(cm)
    md = [f"# {trip} — trip archive", "", f"- Places added during the trip: {len(pins)}", f"- Journal entries: {len(comments)} ({sum(1 for x in comments if x.get('photo_url'))} with photos)", ""]
    if pins:
        md += ["## Places added during the trip", ""] + [f'- **{p["name"]}** ({p["lat"]:.4f}, {p["lng"]:.4f}) — added by {p["added_by"]}, {p["created_at"][:10]}' + (f': {p["notes"]}' if p.get("notes") else "") for p in pins] + [""]
    md += ["## Journal, by place", ""]
    for name, items in by.items():
        md += [f"### {name}", ""]
        for x in items:
            md.append(f'- **{x["author"]}**, {x["created_at"][:16].replace("T", " ")}' + (f': {x["comment_text"]}' if x.get("comment_text") else ""))
            if x.get("local_photo"): md.append(f'  ![[{x["local_photo"]}]]')
        md.append("")
    open(os.path.join(a.out, "summary.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"\nwrote archive to {a.out}")

main()
