#!/usr/bin/python
# coding: utf8

import what3words
from os import environ

# Setup API key
api_key = environ.get("W3W_API_KEY", "your_api_key")
geocoder = what3words.Geocoder(api_key)

# --- Test 1: Convert to Coordinates ---
print("## convert_to_coordinates #########")
res = geocoder.convert_to_coordinates("prom.cape.pump", "geojson")
if "error" in res:
    print(f"API error code: {res['error']['message']}")
else:
    print(res)
print("\n")

# --- Test 2: Convert Coordinates to 3 Word Address ---
print("## convert_to_3wa #########")
coordinates = what3words.Coordinates(51.484463, -0.195405)
res = geocoder.convert_to_3wa(coordinates)
print(res)
print("\n")

# --- Test 3: Grid Section ---
print("## grid_section #########")
sw = what3words.Coordinates(52.207988, 0.116126)
ne = what3words.Coordinates(52.208867, 0.117540)
bb = what3words.BoundingBox(sw, ne)
res = geocoder.grid_section(bb)
print(res)
print("\n")

# --- Test 4: Available Languages ---
print("## available_languages #########")
res = geocoder.available_languages()
print(res)
print("\n")

# --- Test 5: AutoSuggest with Limited Results ---
print("## AutoSuggest (limited results) #########")
res = geocoder.autosuggest("filled.count.soap", n_results=3)
print(res)
print("\n")

# --- Test 6: AutoSuggest with Clipping to Country ---
print("## AutoSuggest (clipped to countries) #########")
res = geocoder.autosuggest("filled.count.soap", clip_to_country="fr,de")
print(res)
print("\n")

# --- Test 7: AutoSuggest with Focused Results ---
print("## AutoSuggest with focus #########")
res = geocoder.autosuggest(
    "filled.count.soap",
    focus=what3words.Coordinates(51.520833, -0.195543),
    n_focus_results=1,
    n_results=3,
)
print(res)
print("\n")

# --- Test 8: Check if a text is a valid What3Words address ---
print("## is_valid_3wa #########")
valid_3wa = "index.home.raft"
invalid_3wa = "word.word.word"
print(f"Is '{valid_3wa}' a valid 3WA? {geocoder.is_valid_3wa(valid_3wa)}")
print(f"Is '{invalid_3wa}' a valid 3WA? {geocoder.is_valid_3wa(invalid_3wa)}")
print("\n")

# --- Test 9: Check if text could be a valid 3-word address ---
print("## is_possible_3wa #########")
possible_3wa = "index.home.raft"
invalid_format_3wa = "index.home"
print(f"Is '{possible_3wa}' a possible 3WA? {geocoder.is_possible_3wa(possible_3wa)}")
print(
    f"Is '{invalid_format_3wa}' a possible 3WA? {geocoder.is_possible_3wa(invalid_format_3wa)}"
)
print("\n")

# --- Test 10: Did You Mean (approximate match) ---
print("## did_you_mean #########")
near_miss_3wa = "indx.home.rafe"
print(
    f"Did you mean a 3WA for '{near_miss_3wa}'? {geocoder.did_you_mean(near_miss_3wa)}"
)
print("\n")

# --- Test 11: Find all possible 3WA in text ---
print("## find_possible_3wa #########")
sample_text = "Here are some addresses: index.home.raft and index.home.shelf"
possible_3was = geocoder.find_possible_3wa(sample_text)
print(f"Possible 3WAs in text: {possible_3was}")
print("\n")
