#!/usr/bin/python
# coding: utf8

import json
import requests
import platform
import re

from .version import __version__

class Geocoder(object):
    """
    What3Words v3 API wrapper
    ==========
    """

    def __init__(self, api_key, language='en',
                 end_point='https://api.what3words.com/v3'):
        """
        Constructor
        Params
        ------
        :param api_key: A valid API key
        :param language: default langauge use with the Geocoder
        :param end_point: what3words api end point
        """

        self.end_point = end_point
        self.api_key = api_key
        self.language = language

    def convert_to_coordinates(self, words, format='json'):
        """
        Take a 3 word address and turn it into a pair of coordinates.

        Params
        ------
        :param string words: A 3 word address as a string
        :param string format: Return data format type; can be one of
                              json (the default), geojson

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v3/#convert-to-coordinates
        """

        params = {
            'words': words,
            'format': format,
        }

        return self._request('/convert-to-coordinates', params)

    def convert_to_3wa(self, coordinates, format='json', language=None):
        """
        Take latitude and longitude coordinates and turn them into
        a 3 word address.

        Params
        ------
        :param Coordinates coordinates: the coordinates of the location to convert to 3 word address
        :param float lng: longitude coordinate
        :param string format: Return data format type; can be one of
                              json (the default), geojson
        :param string language: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.language

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v3/#convert-to-3wa
        """

        params = {
            'coordinates': '{0},{1}'.format(coordinates.lat, coordinates.lng),
            'format': format,
            'language': language or self.language,
        }
        return self._request('/convert-to-3wa', params)

    def grid_section(self, bounding_box, format='json'):
        """
        Take latitude and longitude coordinates and turn them into
        a 3 word address.

        Params
        ------
        :param BoundingBox bbox: Bounding box, specified by the northeast and
                            southwest corner coordinates, for which the grid
                            should be returned.
        :param string format: Return data format type; can be one of
                              json (the default), geojson
        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v3/#grid-section
        """

        params = {
            'bounding-box': '{0},{1},{2},{3}'.format(bounding_box.sw.lat, bounding_box.sw.lng, bounding_box.ne.lat, bounding_box.ne.lng),
            'format': format
        }
        return self._request('/grid-section', params)

    def available_languages(self):
        """
        Retrieve a list of available 3 word languages.

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v3/#available-languages
        """

        return self._request('/available-languages')

    def autosuggest(self, 
        input, 
        n_results=None, 
        focus=None, 
        n_focus_results=None,
        clip_to_country=None,
        clip_to_bounding_box=None,
        clip_to_circle=None,
        clip_to_polygon=None,
        input_type=None,
        language=None):
        """
        Returns a list of 3 word addresses based on user input and other
        parameters.

        Params
        ------
        :param string input: The full or partial 3 word address to obtain
                            suggestions for. At minimum this must be the
                            first two complete words plus at least one
                            character from the third word
        :param int n_results: The number of AutoSuggest results to return. A maximum of 100 
                            results can be specified, if a number greater than this is 
                            requested, this will be truncated to the maximum. The default is 3
        :param Coordinates focus: A location, specified as a latitude,longitude used
                            to refine the results. If specified, the results
                            will be weighted to give preference to those near
                            the specified location in addition to considering
                            similarity to the suggest string. If omitted the
                            default behaviour is to weight results for
                            similarity to the suggest string only.
        :param int n_focus_results: Specifies the number of results (must be <= n_results) 
                            within the results set which will have a focus. Defaults to 
                            n_results. This allows you to run autosuggest with a mix of 
                            focussed and unfocussed results, to give you a "blend" of the two.
        :param string clip_to_country: Restricts autosuggest to only return results inside the 
                            countries specified by comma-separated list of uppercase ISO 3166-1 
                            alpha-2 country codes (for example, to restrict to Belgium and the 
                            UK, use clip_to_country="GB,BE")
        :param BoundingBox clip_to_bounding_box: Restrict autosuggest results to a bounding 
                            box, specified by coordinates.
        :param Circle clip_to_circle: Restrict autosuggest results to a circle, specified by 
                            Coordinates representing the center of the circle, and a distance in 
                            kilometres which represents the radius. For convenience, longitude 
                            is allowed to wrap around 180 degrees. For example 181 is equivalent 
                            to -179.
        :param Coordinates[] clip_to_polygon: Restrict autosuggest results to a polygon, 
                            specified by a list of Coordinates. The polygon 
                            should be closed, i.e. the first element should be repeated as the 
                            last element; also the list should contain at least 4 entries. 
                            The API is currently limited to accepting up to 25 pairs.
        :param string input_type: For power users, used to specify voice input mode. Can be 
                            text (default), vocon-hybrid or nmdp-asr.
        :param string language: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.language

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#autosuggest
        """

        params = {
            'input': input,
            'language': language or self.language,
        }
        if n_results:
            params.update({
                'n-results': '{0}'.format(n_results)
            })
        if focus:
            params.update({
                'focus': '{0},{1}'.format(focus.lat, focus.lng)
            })
        if n_focus_results:
            params.update({
                'n-focus-results': '{0}'.format(n_focus_results)
            })
        if clip_to_country:
            params.update({
                'clip-to-country': '{0}'.format(clip_to_country)
            })
        if clip_to_bounding_box:
            params.update({
                'clip-to-bounding-box': '{0},{1},{2},{3}'.format(clip_to_bounding_box.sw.lat, clip_to_bounding_box.sw.lng, clip_to_bounding_box.ne.lat, clip_to_bounding_box.ne.lng)
            })
        if clip_to_circle:
            params.update({
                'clip-to-circle': '{0},{1},{2}'.format(clip_to_circle.center.lat, clip_to_circle.center.lng, clip_to_circle.radius)
            })
        if clip_to_polygon:
            params.update({
                'clip-to-polygon': '{0}'.format(', '.join("{},{}".format(coord.lat, coord.lng) for coord in clip_to_polygon))
            })
        if input_type:
            params.update({
                'input-type': '{0}'.format(','.join(input_type))
            })

        return self._request('/autosuggest', params)

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

        headers = {'X-W3W-Wrapper': 'what3words-Python/{} (Python {}; {})'.format(__version__, platform.python_version(), platform.platform())}
        r = requests.get(url, params=params, headers=headers)
        response = r.text
        return json.loads(response)

class Coordinates(object):
    """
    A Coordinate represents (latitude, longitude) coordinates encoded according to the World Geodetic System (WGS84).
    ==========
    """

    def __init__(self,lat,lng):
        """
        Constructor
        Params
        ------
        :param lat: the latitude
        :param lng: the longitude
        """
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        return self.lng == other.lng and self.lat == other.lat

    def __str__(self):
        return '<{0}, {1}>'.format(self.lat, self.lng)
    
    def __repr__(self):
        return 'Coordinate({0}, {1})'.format(self.lat, self.lng)

class BoundingBox(object):
    """
    A BoundingBox represents which which represents a range of latitudes and longitudes.
    ==========
    """

    def __init__(self,sw,ne):
        """
        Constructor
        Params
        ------
        :param sw: the coordinates of the southwest corner
        :param ne: the coordinates of the northeast corner
        """
        self.sw = sw
        self.ne = ne

    def __eq__(self, other):
        return self.sw == other.sw and self.ne == other.ne
        
    def __str__(self):
        return '<{0}, {1}>'.format(self.sw, self.ne)
    
    def __repr__(self):
        return 'BoundingBox({0}, {1})'.format(repr(self.sw), repr(self.ne))

class Circle(object):
    """
    A Circle represented by center Coordinates, and a radius in kilometres
    ==========
    """

    def __init__(self,center,radius):
        """
        Constructor
        Params
        ------
        :param sw: the coordinates of the southwest corner
        :param ne: the coordinates of the northeast corner
        """
        self.center = center
        self.radius = radius

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius
        
    def __str__(self):
        return '<{0}, {1}>'.format(self.center, self.radius)
    
    def __repr__(self):
        return 'BoundingBox({0}, {1})'.format(repr(self.center), repr(self.radius))
