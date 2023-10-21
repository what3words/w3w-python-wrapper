#!/usr/bin/python
# coding: utf8

import json
import requests
import platform
import re

from .version import __version__


class Coordinates(object):
    """
    A Coordinate represents (latitude, longitude) coordinates encoded according to the World Geodetic System (WGS84).
    ==========
    """

    def __init__(self, lat: float, lng: float) -> None:
        """
        Constructor
        Params
        ------
        :param float lat: the latitude in decimal form
        :param float lng: the longitude in decimal form
        """
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        return self.lng == other.lng and self.lat == other.lat

    def __str__(self):
        return f"<{self.lat}, {self.lng}>"

    def __repr__(self):
        return f"Coordinate({self.lat}, {self.lng})"


class BoundingBox(object):
    """
    A BoundingBox represents which which represents a range of latitudes and longitudes.
    ==========
    """

    def __init__(self, sw: Coordinates, ne: Coordinates):
        """
        Constructor
        Params
        ------
        :param Coordinates sw: the coordinates of the southwest corner
        :param Coordinates ne: the coordinates of the northeast corner
        """
        self.sw = sw
        self.ne = ne

    def __eq__(self, other):
        return self.sw == other.sw and self.ne == other.ne

    def __str__(self):
        return f"<{self.sw}, {self.ne}>"

    def __repr__(self):
        return f"BoundingBox({repr(self.sw)}, {repr(self.ne)})"


class Circle(object):
    """
    A Circle represented by center Coordinates, and a radius in kilometres
    ==========
    """

    def __init__(self, center: Coordinates, radius: float):
        """
        Constructor
        Params
        ------
        :param Coordinates sw: the coordinates of the southwest corner
        :param float radius: the radius of the circle in kilometers
        """
        self.center = center
        self.radius = radius

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    def __str__(self):
        return f"<{self.center}, {self.radius}>"

    def __repr__(self):
        return f"Circle({repr(self.center)}, {repr(self.radius)})"


class Geocoder(object):
    """
    What3Words v3 API wrapper
    ==========
    """

    def __init__(
        self,
        api_key: str,
        language: str = "en",
        end_point: str = "https://api.what3words.com/v3",
    ) -> None:
        """
        Constructor
        Params
        ------
        :param string api_key: A valid API key
        :param string language: default langauge use with the Geocoder
        :param string end_point: what3words api end point
        """

        self.end_point = end_point
        self.api_key = api_key
        self.language = language

    def convert_to_coordinates(self, words: str, format: str = "json") -> dict:
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
            "words": words,
            "format": format,
        }

        return self._request("/convert-to-coordinates", params)

    def convert_to_3wa(
        self,
        coordinates: Coordinates,
        format: str = "json",
        language: str | None = None,
    ) -> dict:
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
            "coordinates": f"{coordinates.lat},{coordinates.lng}",
            "format": format,
            "language": language or self.language,
        }
        return self._request("/convert-to-3wa", params)

    def grid_section(self, bounding_box: BoundingBox, format: str = "json") -> dict:
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
            "bounding-box": f"{bounding_box.sw.lat},{bounding_box.sw.lng},{bounding_box.ne.lat},{bounding_box.ne.lng}",
            "format": format,
        }
        return self._request("/grid-section", params)

    def available_languages(self) -> dict:
        """
        Retrieve a list of available 3 word languages.

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v3/#available-languages
        """

        return self._request("/available-languages")

    def autosuggest(
        self,
        input: str,
        n_results: int | None = None,
        focus: Coordinates | None = None,
        n_focus_results: int | None = None,
        clip_to_country: str | None = None,
        clip_to_bounding_box: BoundingBox | None = None,
        clip_to_circle: Circle | None = None,
        clip_to_polygon: list[BoundingBox] | None = None,
        input_type: str | None = None,
        language: str | None = None,
        prefer_land: str | None = None,
    ) -> dict:
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
                            text (default), vocon-hybrid, nmdp-asr or generic-voice.
        :param string language: A supported 3 word address language as an
                            ISO 639-1 2 letter code. Defaults to self.language
        :param string prefer_land: Makes autosuggest prefer results on land to those in the sea.
                            This setting is on by default. Use false to disable this setting and
                            receive more suggestions in the sea.

        :rtype: dict

        References
        ----------
        API Reference: https://docs.what3words.com/api/v2/#autosuggest
        """

        params = {
            "input": input,
            "language": language or self.language,
        }
        if n_results:
            params["n-results"] = f"{n_results}"
        if focus:
            params["focus"] = f"{focus.lat},{focus.lng}"
        if n_focus_results:
            params["n-focus-results"] = f"{n_focus_results}"
        if clip_to_country:
            params["clip-to-country"] = f"{clip_to_country}"
        if clip_to_bounding_box:
            params[
                "clip-to-bounding-box"
            ] = f"{clip_to_bounding_box.sw.lat},{clip_to_bounding_box.sw.lng},{clip_to_bounding_box.ne.lat},{clip_to_bounding_box.ne.lng}"
        if clip_to_circle:
            params[
                "clip-to-circle"
            ] = f"{clip_to_circle.center.lat},{clip_to_circle.center.lng},{clip_to_circle.radius}"
        if clip_to_polygon:
            params["clip-to-polygon"] = ", ".join(
                f"{coord.lat},{coord.lng}" for coord in clip_to_polygon
            )
        if input_type:
            params["input-type"] = f"{input_type}"
        if prefer_land:
            params["prefer-land"] = f"{prefer_land}"

        return self._request("/autosuggest", params)

    def defaultLanguage(self, lang: str | None = None) -> str:
        """
        Sets/returns default language

        Params
        ------
        :param string lang: new default language

        :retype: string
        """
        if lang:
            self.language = lang
        return self.language

    def defaultEndpoint(self, end_point: str | None = None) -> str:
        """
        Sets/returns api endpoint

        Params
        ------
        :param string end_point: new api endpoint

        :retype: string url
        """
        if end_point is not None:
            self.end_point = end_point
        return self.end_point

    def _request(
        self,
        url_path: str,
        params: dict | None = None,
    ) -> dict:
        """
        Executes request

        Params
        ------
        :param string url_path: API method URI
        :param dict params: parameters

        :rtype: dict
        """
        if not params:
            params = {}
        params["key"] = self.api_key

        url = self.end_point + url_path

        headers = {
            "X-W3W-Wrapper": f"what3words-Python/{__version__} (Python {platform.python_version()}; {platform.platform()})"
        }
        r = requests.get(url, params=params, headers=headers)
        return r.json()

    def isPossible3wa(self, text: str) -> bool:
        """
        Determines of the string passed in is the form of a three word address.
        This does not validate whther it is a real address as it returns True for x.x.x

        Params
        ------
        :param string text: text to check

        :rtype: bool
        """
        regex_match = "^/*(?:[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}|'<,.>?/\";:£§º©®\s]+[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+|[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]+){1,3})$"
        return not (None == re.match(regex_match, text))

    def findPossible3wa(self, text: str) -> dict:
        """
        Searches the string passed in for all substrings in the form of a three word address.
        This does not validate whther it is a real address as it will return x.x.x as a result

        Params
        ------
        :param string text: text to check

        :rtype: dict
        """
        regex_search = "[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}"
        return re.findall(regex_search, text, flags=re.UNICODE)

    def didYouMean(self, text: str) -> bool:
        """
        Determines of the string passed in is almost in the form of a three word address.
        This will return True for values such as "filled-count-soap" and "filled count soap"

        Params
        ------
        :param string text: text to check

        :rtype: bool
        """
        regex_match = "^/*[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።। ,\\-_/+'&\\:;|　-]{1,2}[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።। ,\\-_/+'&\\:;|　-]{1,2}[^0-9`~!@#$%^&*()+\-_=[{\]}\\|'<,.>?/\";:£§º©®\s]{1,}$"
        return not (None == re.match(regex_match, text))

    def isValid3wa(self, text: str) -> bool:
        """
        Determines of the string passed in is a real three word address.  It calls the API
        to verify it refers to an actual plac eon earth.

        Params
        ------
        :param string text: text to check

        :rtype: bool
        """
        if self.isPossible3wa(text):
            result = self.autosuggest(text, n_results=1)
            if len(result["suggestions"]) > 0:
                if result["suggestions"][0]["words"] == text:
                    return True
        return False
