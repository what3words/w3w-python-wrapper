#!/usr/bin/python
# coding: utf8

import json

import requests


class Geocoder(object):
    """
    What3Words API wrapper
    ==========
    """

    def __init__(self, api_key, lang='en',
                 end_point='https://api.what3words.com/v2'):
        """
        Constructor
        Params
        ------
        :param api_key: A valid API key
        :param lang: default langauge use with the Geocoder
        :param end_point: what3words api end point
        """

        self.end_point = end_point
        self.api_key = api_key
        self.lang = lang

    def forward(self, addr, display='full', format='json', lang=None):
        """
        Take a 3 word address and turn it into a pair of coordinates.

        Params
        ------
        :param string addr: A 3 word address as a string
        :param string lang: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.lang
        :param string display: Return display type; can be one of
                               full (the default) or terse
        :param string format: Return data format type; can be one of
                              json (the default), geojson or xml

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#forward
        """

        params = {
            'addr': addr,
            'display': display,
            'format': format,
            'lang': lang or self.lang,
        }

        return self._request('/forward', params)

    def reverse(self, lat, lng, display='full', format='json', lang=None):
        """
        Take latitude and longitude coordinates and turn them into
        a 3 word address.

        Params
        ------
        :param float lat: latitude coordinate
        :param float lng: longitude coordinate
        :param string display: return the lat and lng coordinates of the
                             south-west and north-east corners of the
                             what3words grid square.
        :param string format: Return data format type; can be one of
                              json (the default), geojson or xml
        :param string lang: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.lang

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#reverse
        """

        params = {
            'coords': '{0},{1}'.format(lat, lng),
            'display': display,
            'format': format,
            'lang': lang or self.lang,
        }
        return self._request('/reverse', params)

    def autosuggest(self, suggest, focus=None, clip=None, display='full',
                    format='json', lang=None):
        """
        Returns a list of 3 word addresses based on user input and other
        parameters.

        Params
        ------
        :param string suggest: The full or partial 3 word address to obtain
                               suggestions for. At minimum this must be the
                               first two complete words plus at least one
                               character from the third word
        :param string focus: A location, specified as a latitude,longitude used
                             to refine the results. If specified, the results
                             will be weighted to give preference to those near
                             the specified location in addition to considering
                             similarity to the suggest string. If omitted the
                             default behaviour is to weight results for
                             similarity to the suggest string only.
        :param string clip: Restricts results to those within a geographical
                            area. If omitted defaults to clip=none
        :param string format: Return data format type; can be one of
                              json (the default), geojson or xml
        :param string lang: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.lang

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#autosuggest
        """

        params = {
            'addr': suggest,
            'display': display,
            'format': format,
            'lang': lang or self.lang,
        }
        if focus:
            params.update({
                'focus': focus
            })
        if clip:
            params.update({
                'clip': clip
            })

        return self._request('/autosuggest', params)

    def standardblend(self, suggest, focus=None, display='full',
                      format='json', lang=None):
        """
        Returns a blend of the three most relevant 3 word address candidates
        for a given location, based on a full or partial 3 word address.

        Params
        ------
        :param string suggest: The full or partial 3 word address to obtain
                               suggestions for. At minimum this must be the
                               first two complete words plus at least one
                               character from the third word
        :param string focus: A location, specified as a latitude,longitude used
                             to refine the results. If specified, the results
                             will be weighted to give preference to those near
                             the specified location in addition to considering
                             similarity to the suggest string. If omitted the
                             default behaviour is to weight results for
                             similarity to the suggest string only.
        :param string format: Return data format type; can be one of
                              json (the default), geojson or xml
        :param string lang: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.lang

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#standardblend
        """

        params = {
            'addr': suggest,
            'display': display,
            'format': format,
            'lang': lang or self.lang,
        }
        if focus:
            params.update({
                'focus': focus
            })

        return self._request('/standardblend', params)

    def grid(self, bbox, display='full', format='json'):
        """
        Take latitude and longitude coordinates and turn them into
        a 3 word address.

        Params
        ------
        :param string bbox: Bounding box, specified by the northeast and
                            southwest corner coordinates, for which the grid
                            should be returned.
        :param string display: return the lat and lng coordinates of the
                             south-west and north-east corners of the
                             what3words grid square.
        :param string format: Return data format type; can be one of
                              json (the default), geojson or xml
        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#grid
        """

        params = {
            'bbox': bbox,
            'display': display,
            'format': format
        }
        return self._request('/grid', params)

    def languages(self):
        """
        Retrieve a list of available 3 word languages.

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#lang
        """

        return self._request('/languages')

    def defaultLanguage(self, lang=None):
        """
        Sets/returns default language

        Params
        ------
        :param string lang: new default language

        :retype: string
        """
        if(lang is not None):
            self.lang = lang
        return self.lang

    def defaultEndpoint(self, end_point=None):
        """
        Sets/returns api endpoint

        Params
        ------
        :param string end_point: new api endpoint

        :retype: string url
        """
        if(end_point is not None):
            self.end_point = end_point
        return self.end_point

    def _request(self, url_path, params=None):
        """
        Executes request

        Params
        ------
        :param string url_path: API method URI
        :param dict params: parameters

        :rtype: dict
        """
        if params is None:
            params = {}

        params.update({
            'key': self.api_key,
        })
        url = self.end_point+url_path
        r = requests.get(url, params=params)
        response = r.text
        return json.loads(response)
