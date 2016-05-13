#!/usr/bin/env python
# coding: utf8
"""
Unit tests for what3words API wrapper lib
"""

import what3words
import json
from os import environ

api_key = environ['W3W_API_KEY']
words = 'daring.lion.race'
lat = 51.508341
lng = -0.125499
corners = [[51.508328, -0.12552], [51.508355, -0.125477]]


def testInvalidKey():
    badkey = 'BADKEY'
    geocoder = what3words.Geocoder(badkey)
    result = geocoder.position(words)
    assert result['error'] == u'X1'
    assert result['message'] == u'Missing or invalid key'


def testForwardGeocode():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.position(words)
    assert result['type'] == u'3 words'
    assert result['language'] == u'en'
    assert result['words'] == [u'daring', u'lion', u'race']
    assert result['position'] == [lat, lng]
    assert result['corners'] == corners


def testReverseGeocode():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.words(lat, lng)
    assert result['language'] == u'en'
    assert result['words'] == [u'daring', u'lion', u'race']
    assert result['position'] == [lat, lng]
    assert result['corners'] == corners


if __name__ == '__main__':
    testInvalidKey()
    testForwardGeocode()
    testReverseGeocode()
