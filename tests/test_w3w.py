#!/usr/bin/env python
# coding: utf8
"""
Unit tests for what3words API wrapper lib
"""

import what3words
import json
import sys
from os import environ

api_key = environ['W3W_API_KEY']
addr = 'daring.lion.race'
lat = 51.508341
lng = -0.125499
english = {'code': 'en', 'name': 'English', 'native_name': 'English'}
suggest = 'indx.home.rqft'

def testInvalidKey():
    badkey = 'BADKEY'
    geocoder = what3words.Geocoder(badkey)
    result = geocoder.convert_to_coordinates(addr)
    assert result['error']['code'] == 'InvalidKey'
    assert result['error']['message'] == 'Authentication failed; invalid API key'


def testConvertToCoordinates():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.convert_to_coordinates(addr)
    assert result['language'] == 'en'
    assert result['words'] == 'daring.lion.race'
    assert result['coordinates']['lat'] == lat
    assert result['coordinates']['lng'] == lng


def testConvertTo3wa():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.convert_to_3wa(what3words.Coordinates(lat, lng))
    assert result['language'] == 'en'
    assert result['words'] == 'daring.lion.race'
    assert result['coordinates']['lat'] == lat
    assert result['coordinates']['lng'] == lng


def testLanguages():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.available_languages()
    assert result['languages'] is not None
    if english in result['languages']:
        assert True
    else:
        assert False


def testAutoSuggest():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.autosuggest(suggest)

    assert result['suggestions'] is not None


def testGrid():
    geocoder = what3words.Geocoder(api_key)
    sw = what3words.Coordinates(52.208867,0.117540)
    ne = what3words.Coordinates(52.207988,0.116126)
    bb = what3words.BoundingBox(sw, ne)

    result = geocoder.grid_section(bb)

    assert result['lines'] is not None


if __name__ == '__main__':
    testInvalidKey()
    # testLanguages()
    # testForwardGeocode()
    # testReverseGeocode()
    # testAutoSuggest()
    # testStandardBlend()
    # testAutoSuggestML()
    # testStandardBlendML()
    # testGrid()
