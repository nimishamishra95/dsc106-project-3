import json
import os

print("Loading grid files...")

with open("cmip6_historical_grid.json") as f:
    raw = f.read()

partial = raw.rfind("},")
grid1 = json.loads(raw[:partial+1] + "]")
print(f"  Truncated file: {len(grid1):,} records (1850–1994)")

with open("grid_1995_2014.json") as f:
    grid2 = json.load(f)
print(f"  Missing chunk:  {len(grid2):,} records (1995–2014)")

grid = grid1 + grid2
print(f"  Combined:       {len(grid):,} records")

for r in grid:
    if r["lon"] > 180:
        r["lon"] = round(r["lon"] - 360, 2)

lons = sorted(set(r["lon"] for r in grid))
years = sorted(set(r["year"] for r in grid))
print(f"\nGrid lon range: {lons[0]} to {lons[-1]}")
print(f"Grid year range: {years[0]}–{years[-1]} ({len(years)} years)")

with open("cmip6_cities.json") as f:
    cities = json.load(f)

for city in cities.values():
    if city["lon"] > 180:
        city["lon"] = round(city["lon"] - 360, 2)

print(f"\nCities: {list(cities.keys())}")

with open("cmip6_grid_clean.json", "w") as f:
    json.dump(grid, f, separators=(",", ":"))

with open("cmip6_cities_clean.json", "w") as f:
    json.dump(cities, f, separators=(",", ":"))

size = os.path.getsize("cmip6_grid_clean.json") / 1e6
print(f"\ncmip6_grid_clean.json   ({size:.1f} MB)")
print(f"cmip6_cities_clean.json  ({os.path.getsize('cmip6_cities_clean.json')/1e3:.1f} KB)")