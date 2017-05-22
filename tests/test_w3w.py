#!/usr/bin/env python
# coding: utf8
"""
Unit tests for what3words API wrapper lib
"""

import what3words
import json
from os import environ

api_key = environ['W3W_API_KEY']
addr = 'daring.lion.race'
lat = 51.508341
lng = -0.125499
english = {u'code': u'en', u'name': u'English', u'native_name': u'English'}
suggest = 'indx.home.rqft'


def testInvalidKey():
    badkey = 'BADKEY'
    geocoder = what3words.Geocoder(badkey)
    result = geocoder.forward(addr)
    assert result['code'] == 2
    assert result['message'] == u'Authentication failed; invalid API key'


def testForwardGeocode():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.forward(addr)
    assert result['language'] == u'en'
    assert result['words'] == u'daring.lion.race'
    assert result['geometry']['lat'] == lat
    assert result['geometry']['lng'] == lng


def testReverseGeocode():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.reverse(lat, lng)
    assert result['language'] == u'en'
    assert result['words'] == u'daring.lion.race'
    assert result['geometry']['lat'] == lat
    assert result['geometry']['lng'] == lng


def testLanguages():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.languages()
    assert result['languages'] is not None
    if english in result['languages']:
        assert True
    else:
        assert False


def testAutoSuggest():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.autosuggest(suggest)

    assert result['suggestions'] is not None


def testAutoSuggestML():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.autosuggest_ml(suggest)

    assert result['suggestions'] is not None


def testStandardBlend():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.standardblend(suggest)

    assert result['blends'] is not None


def testStandardBlendML():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.standardblend_ml(suggest)

    assert result['blends'] is not None


def testGrid():
    geocoder = what3words.Geocoder(api_key)
    result = geocoder.grid("52.208867,0.117540,52.207988,0.116126")

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
