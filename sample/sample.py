#!/usr/bin/python
# coding: utf8

import what3words
from os import environ

api_key = environ['W3W_API_KEY']

geocoder = what3words.Geocoder(api_key)
res = geocoder.position(words='prom.cape.pump')
print(res)
print('\n')

res = geocoder.words(lat='51.484463', lng='-0.195405')
print(res)
print('\n')
