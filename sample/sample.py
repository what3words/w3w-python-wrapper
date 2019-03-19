#!/usr/bin/python
# coding: utf8

import what3words
from os import environ

api_key = environ['W3W_API_KEY']

geocoder = what3words.Geocoder(api_key)

## convert_to_coordinates #########
res = geocoder.convert_to_coordinates('prom.cape.pump', 'geojson')
print(res)
print('\n')

## convert_to_3wa #########
coordinates = what3words.Coordinates(51.484463, -0.195405)
res = geocoder.convert_to_3wa(coordinates)
print(res)
print('\n')

## grid_section #########
sw = what3words.Coordinates(52.207988,0.116126)
ne = what3words.Coordinates(52.208867,0.117540)
bb = what3words.BoundingBox(sw, ne)

res = geocoder.grid_section(bb)
print(res)
print('\n')

## grid_section #########
res = geocoder.available_languages()
print(res)
print('\n')


## Vanilla autosuggest, limiting the number of results to three #########
res = geocoder.autosuggest('filled.count.soap', n_results=3)
print(res)
print('\n')

## autosuggest demonstrating clipping to polygon, circle, bounding box, and country #########
polygon = [
	what3words.Coordinates(52.321911, 1.516113),
	what3words.Coordinates(52.321911, -2.021484),
	what3words.Coordinates(50.345460, -2.021484),
	what3words.Coordinates(52.321911, 1.516113)
]

# res = geocoder.autosuggest('filled.count.soap', clip_to_polygon=polygon)
# res = geocoder.autosuggest('filled.count.soap', clip_to_circle=what3words.Circle(what3words.Coordinates(51.520833, -0.195543), 10))
# res = geocoder.autosuggest('filled.count.soap', clip_to_bounding_box=what3words.BoundingBox(what3words.Coordinates(50.345460, -2.021484), what3words.Coordinates(52.321911, 1.516113)))
res = geocoder.autosuggest('filled.count.soap', clip_to_country="fr,de")
print(res)
print('\n')

## autosuggest with a focus, with that focus only applied to the first result #########
res = geocoder.autosuggest('filled.count.soap', \
		focus=what3words.Coordinates(51.520833, -0.195543), \
		n_focus_results=1, \
		n_results=3 \
)

print(res)
print('\n')

## autosuggest with an input type of VoCon Hybrid #########
res = geocoder.autosuggest('{\"_isInGrammar\":\"yes\",\"_isSpeech\":\"yes\",\"_hypotheses\":[{\"_score\":342516,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6546,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34225,\"_orthography\":\"tend\",\"_conf\":6964,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":43800,\"_orthography\":\"poached\",\"_conf\":6181,\"_endTimeMs\":4060,\"_beginTimeMs\":3220}]},{\"_score\":342631,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6498,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34340,\"_orthography\":\"tent\",\"_conf\":6772,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":43800,\"_orthography\":\"poached\",\"_conf\":6181,\"_endTimeMs\":4060,\"_beginTimeMs\":3220}]},{\"_score\":342668,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6474,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34225,\"_orthography\":\"tend\",\"_conf\":6964,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":41696,\"_orthography\":\"perch\",\"_conf\":5950,\"_endTimeMs\":4020,\"_beginTimeMs\":3220}]},{\"_score\":342670,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6474,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34379,\"_orthography\":\"tinge\",\"_conf\":6705,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":43800,\"_orthography\":\"poached\",\"_conf\":6181,\"_endTimeMs\":4060,\"_beginTimeMs\":3220}]},{\"_score\":342783,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6426,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34340,\"_orthography\":\"tent\",\"_conf\":6772,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":41696,\"_orthography\":\"perch\",\"_conf\":5950,\"_endTimeMs\":4020,\"_beginTimeMs\":3220}]},{\"_score\":342822,\"_startRule\":\"whatthreewordsgrammar#_main_\",\"_conf\":6402,\"_endTimeMs\":6360,\"_beginTimeMs\":1570,\"_lmScore\":300,\"_items\":[{\"_type\":\"terminal\",\"_score\":34379,\"_orthography\":\"tinge\",\"_conf\":6705,\"_endTimeMs\":2250,\"_beginTimeMs\":1580},{\"_type\":\"terminal\",\"_score\":47670,\"_orthography\":\"artichokes\",\"_conf\":7176,\"_endTimeMs\":3180,\"_beginTimeMs\":2260},{\"_type\":\"terminal\",\"_score\":41696,\"_orthography\":\"perch\",\"_conf\":5950,\"_endTimeMs\":4020,\"_beginTimeMs\":3220}]}],\"_resultType\":\"NBest\"}', \
		input_type='vocon-hybrid', \
		language='en'
)

print(res)
print('\n')
