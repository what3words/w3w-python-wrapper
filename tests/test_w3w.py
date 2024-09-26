#!/usr/bin/env python
# coding: utf8
"""
Unit tests for what3words API wrapper lib
"""

import what3words
from os import environ
from unittest import TestCase

API_KEY = environ["W3W_API_KEY"]
ADDR = "daring.lion.race"
LAT = 51.508341
LNG = -0.125499
ENGLISH_DICT = {"code": "en", "name": "English", "nativeName": "English"}
SUGGEST = "indx.home.rqft"
WHAT3WORDS_MAPPING = {ADDR: what3words.Coordinates(LAT, LNG)}


class TestCases(TestCase):
    def setUp(self):
        self.geocoder = what3words.Geocoder(API_KEY)

    def test_invalid_key(self):
        self.geocoder.api_key = "BADKEY"
        result = self.geocoder.convert_to_coordinates(ADDR)
        assert result["error"]["code"] == "InvalidKey"
        assert result["error"]["message"] == "Authentication failed; invalid API key"

    def test_convert_to_coordinates(self):
        result = self.geocoder.convert_to_coordinates(ADDR)
        assert result["language"] == "en"
        assert result["words"] == ADDR
        assert result["coordinates"]["lat"] == WHAT3WORDS_MAPPING[ADDR].lat
        assert result["coordinates"]["lng"] == WHAT3WORDS_MAPPING[ADDR].lng

    def test_convert_to_3wa(self):
        result = self.geocoder.convert_to_3wa(WHAT3WORDS_MAPPING[ADDR])
        assert result["language"] == "en"
        assert result["words"] == ADDR
        assert result["coordinates"]["lat"] == WHAT3WORDS_MAPPING[ADDR].lat
        assert result["coordinates"]["lng"] == WHAT3WORDS_MAPPING[ADDR].lng

    def test_languages(self):
        result = self.geocoder.available_languages()
        assert result["languages"] is not None
        assert ENGLISH_DICT in result["languages"]

    def testAutoSuggest(self):
        result = self.geocoder.autosuggest(SUGGEST)
        assert result["suggestions"] is not None

    def testGrid(self):
        sw = what3words.Coordinates(52.208867, 0.117540)
        ne = what3words.Coordinates(52.207988, 0.116126)
        bb = what3words.BoundingBox(sw, ne)

        result = self.geocoder.grid_section(bb)

        assert result["lines"] is not None
