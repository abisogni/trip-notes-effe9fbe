-- Copenhagen Trip Journal — Supabase setup
-- Already applied (migration "copenhagen_trip_tables") to the shared
-- paris-trip-2026 Supabase project. Kept here for reference / re-creation.
-- Photos are stored in Cloudinary, not Supabase Storage.

create table public.copenhagen_pins (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  lat double precision not null,
  lng double precision not null,
  notes text,
  source_url text,
  added_by text not null,
  created_at timestamptz not null default now()
);

create table public.copenhagen_comments (
  id uuid primary key default gen_random_uuid(),
  pin_id text not null,
  pin_name text not null,
  author text not null,
  comment_text text,
  photo_url text,
  created_at timestamptz not null default now()
);

create index on public.copenhagen_comments (pin_id);

-- Append-only: anyone with the anon key can read and add, not edit/delete.
alter table public.copenhagen_pins enable row level security;
alter table public.copenhagen_comments enable row level security;

create policy "public read copenhagen_pins" on public.copenhagen_pins for select using (true);
create policy "public insert copenhagen_pins" on public.copenhagen_pins for insert with check (true);
create policy "public read copenhagen_comments" on public.copenhagen_comments for select using (true);
create policy "public insert copenhagen_comments" on public.copenhagen_comments for insert with check (true);

alter publication supabase_realtime add table public.copenhagen_pins;
alter publication supabase_realtime add table public.copenhagen_comments;
