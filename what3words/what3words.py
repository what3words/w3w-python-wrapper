#!/usr/bin/python
# coding: utf8

import json
import requests
import platform
import re
from typing import List, Optional, Dict

from .version import __version__


class Geocoder:
    """
    What3Words v3 API wrapper
    """

    def __init__(
        self,
        api_key: str,
        language: str = "en",
        end_point: str = "https://api.what3words.com/v3",
    ):
        """
        Constructor
        :param api_key: A valid API key
        :param language: Default language used with the Geocoder
        :param end_point: What3Words API endpoint
        """
        self.end_point = end_point
        self.api_key = api_key
        self.language = language

    def convert_to_coordinates(
        self, words: str, format: str = "json", locale: Optional[str] = None
    ) -> Dict:
        """
        Convert a 3 word address into coordinates.
        :param words: A 3 word address as a string
        :param format: Return data format type; can be 'json' (default) or 'geojson'
        :param locale: A supported locale as an ISO 639-1 2 letter code
        :return: Response as a dictionary
        """
        params = {"words": words, "format": format, "locale": locale}
        if locale:
            params["locale"] = locale
        response = self._request("/convert-to-coordinates", params)
        if "error" in response:
            return {"error": response["error"]}
        return response

    def convert_to_3wa(
        self,
        coordinates: "Coordinates",
        format: str = "json",
        language: Optional[str] = None,
        locale: Optional[str] = None,
    ) -> Dict:
        """
        Convert latitude and longitude coordinates into a 3 word address.
        :param coordinates: Coordinates object
        :param format: Return data format type; can be 'json' (default) or 'geojson'
        :param language: A supported 3 word address language as an ISO 639-1 2 letter code. Defaults to self.language
        :param locale: A supported locale as an ISO 639-1 2 letter code
        :return: Response as a dictionary
        """
        params = {
            "coordinates": f"{coordinates.lat},{coordinates.lng}",
            "format": format,
            "language": language or self.language,
            "locale": locale,
        }
        if locale:
            params["locale"] = locale

        response = self._request("/convert-to-3wa", params)
        if "error" in response:
            return {"error": response["error"]}
        return response

    def grid_section(self, bounding_box: "BoundingBox", format: str = "json") -> Dict:
        """
        Retrieve a grid section for a bounding box.
        :param bounding_box: BoundingBox object
        :param format: Return data format type; can be 'json' (default) or 'geojson'
        :return: Response as a dictionary
        """
        params = {
            "bounding-box": f"{bounding_box.sw.lat},{bounding_box.sw.lng},{bounding_box.ne.lat},{bounding_box.ne.lng}",
            "format": format,
        }
        response = self._request("/grid-section", params)
        if "error" in response:
            return {"error": response["error"]}
        return response

    def available_languages(self) -> Dict:
        """
        Retrieve a list of available 3 word languages.
        :return: Response as a dictionary
        """
        response = self._request("/available-languages")
        if "error" in response:
            return {"error": response["error"]}
        return response

    def autosuggest(
        self,
        input: str,
        n_results: Optional[int] = None,
        focus: Optional["Coordinates"] = None,
        n_focus_results: Optional[int] = None,
        clip_to_country: Optional[str] = None,
        clip_to_bounding_box: Optional["BoundingBox"] = None,
        clip_to_circle: Optional["Circle"] = None,
        clip_to_polygon: Optional[List["Coordinates"]] = None,
        input_type: Optional[str] = None,
        language: Optional[str] = None,
        prefer_land: Optional[bool] = None,
        locale: Optional[str] = None,
    ) -> Dict:
        """
        Returns a list of 3 word addresses based on user input and other parameters.
        :param input: The full or partial 3 word address to obtain suggestions for
        :param n_results: The number of AutoSuggest results to return (max 100)
        :param focus: Coordinates object used to refine the results
        :param n_focus_results: Number of results within the results set which will have a focus
        :param clip_to_country: Restricts autosuggest to only return results inside specified countries
        :param clip_to_bounding_box: Restrict autosuggest results to a bounding box
        :param clip_to_circle: Restrict autosuggest results to a circle
        :param clip_to_polygon: Restrict autosuggest results to a polygon
        :param input_type: Specify voice input mode
        :param language: A supported 3 word address language as an ISO 639-1 2 letter code
        :param prefer_land: Makes autosuggest prefer results on land to those in the sea
        :param locale: A supported locale as an ISO 639-1 2 letter code
        :return: Response as a dictionary
        """
        params = {"input": input, "language": language or self.language}
        if n_results:
            params["n-results"] = str(n_results)
        if focus:
            params["focus"] = f"{focus.lat},{focus.lng}"
        if n_focus_results:
            params["n-focus-results"] = str(n_focus_results)
        if clip_to_country:
            params["clip-to-country"] = clip_to_country
        if clip_to_bounding_box:
            params["clip-to-bounding-box"] = (
                f"{clip_to_bounding_box.sw.lat},{clip_to_bounding_box.sw.lng},{clip_to_bounding_box.ne.lat},{clip_to_bounding_box.ne.lng}"
            )
        if clip_to_circle:
            params["clip-to-circle"] = (
                f"{clip_to_circle.center.lat},{clip_to_circle.center.lng},{clip_to_circle.radius}"
            )
        if clip_to_polygon:
            params["clip-to-polygon"] = ",".join(
                f"{coord.lat},{coord.lng}" for coord in clip_to_polygon
            )
        if input_type:
            params["input-type"] = input_type
        if prefer_land is not None:
            params["prefer-land"] = str(prefer_land).lower()
        if locale:
            params["locale"] = locale
        response = self._request("/autosuggest", params)
        if "error" in response:
            return {"error": response["error"]}
        return response

    def default_language(self, lang: Optional[str] = None) -> str:
        """
        Sets/returns default language
        :param lang: New default language
        :return: Current default language
        """
        if lang:
            self.language = lang
        return self.language

    def default_endpoint(self, end_point: Optional[str] = None) -> str:
        """
        Sets/returns API endpoint
        :param end_point: New API endpoint
        :return: Current API endpoint
        """
        if end_point:
            self.end_point = end_point
        return self.end_point

    def _request(self, url_path: str, params: Optional[Dict] = None) -> Dict:
        """
        Executes request
        :param url_path: API method URI
        :param params: Parameters
        :return: Response as a dictionary
        """
        if params is None:
            params = {}

        params["key"] = self.api_key
        url = self.end_point + url_path
        headers = {
            "X-W3W-Wrapper": f"what3words-Python/{__version__} (Python {platform.python_version()}; {platform.platform()})"
        }
        response = requests.get(url, params=params, headers=headers).text
        return json.loads(response)

    def is_possible_3wa(self, text: str) -> bool:
        """
        Determines if the string passed in is in the form of a three word address.
        :param text: Text to check
        :return: True if possible 3 word address, False otherwise
        """
        regex_match = r"^\/*(?:[^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}|[<.,>?\/\";:£§º©®\s]+[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+|[^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+){1,3}[.｡。･・︒។։။۔።।][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+([\u0020\u00A0][^0-9`~!@#$%^&*()+\-_=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]+){1,3})$"
        return re.match(regex_match, text) is not None

    def find_possible_3wa(self, text: str) -> List[str]:
        """
        Searches the string passed in for all substrings in the form of a three word address.
        :param text: Text to check
        :return: List of possible 3 word addresses
        """
        regex_search = r"[^\d`~!@#$%^&*()+\-=\[\]{}\\|'<>.,?\/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^\d`~!@#$%^&*()+\-=\[\]{}\\|'<>.,?\/\";:£§º©®\s]{1,}[.｡。･・︒។։။۔።।][^\d`~!@#$%^&*()+\-=\[\]{}\\|'<>.,?\/\";:£§º©®\s]{1,}"
        return re.findall(regex_search, text, flags=re.UNICODE)

    def did_you_mean(self, text: str) -> bool:
        """
        Determines if the string passed in is almost in the form of a three word address.
        :param text: Text to check
        :return: True if almost a 3 word address, False otherwise
        """
        regex_didyoumean = r"^\/?[^0-9`~!@#$%^&*()+\-=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}[.\uFF61\u3002\uFF65\u30FB\uFE12\u17D4\u0964\u1362\u3002:။^_۔։ ,\\\/+'&\\:;|\u3000-]{1,2}[^0-9`~!@#$%^&*()+\-=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}[.\uFF61\u3002\uFF65\u30FB\uFE12\u17D4\u0964\u1362\u3002:။^_۔։ ,\\\/+'&\\:;|\u3000-]{1,2}[^0-9`~!@#$%^&*()+\-=\[\{\]}\\|'<>.,?\/\";:£§º©®\s]{1,}$"
        return re.match(regex_didyoumean, text) is not None

    def is_valid_3wa(self, text: str) -> bool:
        """
        Determines if the string passed in is a real three word address by calling the API.
        :param text: Text to check
        :return: True if valid 3 word address, False otherwise
        """
        if self.is_possible_3wa(text):
            result = self.autosuggest(text, n_results=1)
            if result["suggestions"] and result["suggestions"][0]["words"] == text:
                return True
        return False


class Coordinates:
    """
    A Coordinate represents (latitude, longitude) coordinates encoded according to the World Geodetic System (WGS84).
    """

    def __init__(self, lat: float, lng: float):
        """
        Constructor
        :param lat: Latitude
        :param lng: Longitude
        """
        self.lat = lat
        self.lng = lng

    def __eq__(self, other: "Coordinates") -> bool:
        return self.lng == other.lng and self.lat == other.lat

    def __str__(self) -> str:
        return f"<{self.lat}, {self.lng}>"

    def __repr__(self) -> str:
        return f"Coordinates({self.lat}, {self.lng})"


class BoundingBox:
    """
    A BoundingBox represents a range of latitudes and longitudes.
    """

    def __init__(self, sw: Coordinates, ne: Coordinates):
        """
        Constructor
        :param sw: Coordinates of the southwest corner
        :param ne: Coordinates of the northeast corner
        """
        self.sw = sw
        self.ne = ne

    def __eq__(self, other: "BoundingBox") -> bool:
        return self.sw == other.sw and self.ne == other.ne

    def __str__(self) -> str:
        return f"<{self.sw}, {self.ne}>"

    def __repr__(self) -> str:
        return f"BoundingBox({repr(self.sw)}, {repr(self.ne)})"


class Circle:
    """
    A Circle represented by center Coordinates, and a radius in kilometers.
    """

    def __init__(self, center: Coordinates, radius: float):
        """
        Constructor
        :param center: Coordinates of the center of the circle
        :param radius: Radius of the circle in kilometers
        """
        self.center = center
        self.radius = radius

    def __eq__(self, other: "Circle") -> bool:
        return self.center == other.center and self.radius == other.radius

    def __str__(self) -> str:
        return f"<{self.center}, {self.radius}>"

    def __repr__(self) -> str:
        return f"Circle({repr(self.center)}, {self.radius})"
