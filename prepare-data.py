"""
CMIP6 D3 Data Preprocessor
============================
Run this locally (or in Colab) after downloading your JSON files.
Merges the truncated grid with the missing chunk, converts lon to -180/180,
and outputs two clean files ready for the D3 visualization.

Input files (put in same directory as this script):
    cmip6_historical_grid.json   (truncated, 1850-1994)
    grid_1995_2014.json          (missing chunk, 1995-2014)
    cmip6_cities.json            (10 city timeseries)

Output files:
    cmip6_grid_clean.json        (full 1850-2014 grid, lon -180 to 180)
    cmip6_cities_clean.json      (cities with lon -180 to 180)
"""

import json
import os

# ── 1. Merge grid files ────────────────────────────────────────

print("Loading grid files...")

with open("cmip6_historical_grid.json") as f:
    raw = f.read()

# Recover truncated file (cut off at 32MB)
partial = raw.rfind("},")
grid1 = json.loads(raw[:partial+1] + "]")
print(f"  Truncated file: {len(grid1):,} records (1850–1994)")

with open("grid_1995_2014.json") as f:
    grid2 = json.load(f)
print(f"  Missing chunk:  {len(grid2):,} records (1995–2014)")

grid = grid1 + grid2
print(f"  Combined:       {len(grid):,} records")

# ── 2. Convert lon 0–360 → -180–180 ───────────────────────────

for r in grid:
    if r["lon"] > 180:
        r["lon"] = round(r["lon"] - 360, 2)

lons = sorted(set(r["lon"] for r in grid))
years = sorted(set(r["year"] for r in grid))
print(f"\nGrid lon range: {lons[0]} to {lons[-1]}")
print(f"Grid year range: {years[0]}–{years[-1]} ({len(years)} years)")

# ── 3. Fix cities lon ──────────────────────────────────────────

with open("cmip6_cities.json") as f:
    cities = json.load(f)

for city in cities.values():
    if city["lon"] > 180:
        city["lon"] = round(city["lon"] - 360, 2)

print(f"\nCities: {list(cities.keys())}")

# ── 4. Save ────────────────────────────────────────────────────

with open("cmip6_grid_clean.json", "w") as f:
    json.dump(grid, f, separators=(",", ":"))

with open("cmip6_cities_clean.json", "w") as f:
    json.dump(cities, f, separators=(",", ":"))

size = os.path.getsize("cmip6_grid_clean.json") / 1e6
print(f"\n✅ cmip6_grid_clean.json   ({size:.1f} MB)")
print(f"✅ cmip6_cities_clean.json  ({os.path.getsize('cmip6_cities_clean.json')/1e3:.1f} KB)")
print("\nPlace both files in the same folder as index.html and open in a browser.")