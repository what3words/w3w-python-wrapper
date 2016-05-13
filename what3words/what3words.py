#!/usr/bin/python
# coding: utf8

import json

from requests.compat import urljoin
import requests

__all__ = ('__version__', 'What3Words')

__version__ = (0, 0, 4)


class Geocoder(object):
    """
    What3Words API wrapper
    ==========

    """

    def __init__(self, api_key, lang='en', host='api.what3words.com'):

        self.host = 'https://{0}'.format(host)
        self.api_key = api_key
        self.lang = lang

    def position(self, words, corners=False, lang=None):
        """
        Take a 3 word address and turn it into a pair of coordinates.

        Params
        ------
        :param words: 3 word address
        :type words: list, tuple or str
        :param bool corners: return the lat and lng coordinates of the
                             south-west and north-east corners of the
                             what3words grid square.
        :param lang: response language

        :rtype: dict

        References
        ----------
        API Reference: http://developer.what3words.com/api/#3toposition
        """

        if isinstance(words, (list, tuple)):
            words = '.'.join(words)

        params = {
            'corners': 'true' if corners else 'false',
            'string': words,
            'lang': lang or self.lang,
        }

        return self._request('/w3w', params)

    def words(self, lat, lng, corners=False, lang='en'):
        """
        Take latitude and longitude coordinates and turn them into
        a 3 word address.

        Params
        ------
        :param float lat: latitude coordinate
        :param float lng: longitude coordinate
        :param bool corners: return the lat and lng coordinates of the
                             south-west and north-east corners of the
                             what3words grid square.
        :param lang: response language

        :rtype: dict

        References
        ----------
        API Reference: http://developer.what3words.com/api/#positionto3
        """

        params = {
            'position': '{0},{1}'.format(lat, lng),
            'corners': 'true' if corners else 'false',
            'lang': lang or self.lang,
        }

        return self._request('/position', params)

    def languages(self):
        """
        Retrieve a list of available 3 word languages.

        :rtype: dict

        References
        ----------
        API Reference: http://developer.what3words.com/api/#getlanguages
        """

        return self._request('/get-languages')

    def _request(self, url_path, params=None):
        if params is None:
            params = {}

        params.update({
            'key': self.api_key,
        })
        url = urljoin(self.host, url_path)
        r = requests.get(url, params=params)
        response = r.text
        return json.loads(response)
