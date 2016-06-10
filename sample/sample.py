#!/usr/bin/python
# coding: utf8

import what3words
from os import environ

api_key = environ['W3W_API_KEY']

geocoder = what3words.Geocoder(api_key)
res = geocoder.languages()
print(res)
print('\n')

res = geocoder.forward('prom.cape.pump')
print(res)
print('\n')

res = geocoder.reverse(lat=51.484463, lng=-0.195405)
print(res)
print('\n')

res = geocoder.autosuggest('indx.home.rqft')
print(res)
print('\n')
