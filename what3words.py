import json

from requests.compat import urljoin
import requests

__all__ = ('__version__', 'What3Words')

__version__ = (0, 0, 1)


class What3Words(object):
    """What3Words API"""

    def __init__(self, api_key, host='api.what3words.com', lang='en'):
        self.host = 'http://{0}'.format(host)
        self.api_key = api_key
        self.lang = lang

    def position(self, words, corners=False, lang=None, one_word_password=None,
                 email=None, password=None):
        """Take a 3 word address and turn it into a pair of coordinates.

        :param words: 3 word address
        :type words: list, tuple or str
        :param bool corners: return the lat and lng coordinates of the south-west
            and north-east corners of the what3words grid square.
        :param lang: response language
        :param one_word_password: password for OneWord service
        :type one_word_password: str or None
        :param email: E-mail for OneWord service if required
        :type email: str or None
        :param password: Password for OneWord service if required
        :type password: str or None
        :reference: http://developer.what3words.com/api/#3toposition
        :rtype: dict
        """

        if isinstance(words, (list, tuple)):
            words = '.'.join(words)

        params = {
            'corners': 'true' if corners else 'false',
            'string': words,
            'lang': lang or self.lang,
        }

        if one_word_password is not None:
            params.update({
                'onewordpassword': one_word_password,
                'email': email,
                'password': password,
            })

        return self._request('/w3w', params)

    def words(self, lat, lng, corners=False, lang='en'):
        """Take latitude and longitude coordinates and turn them into a 3 word address.

        :param float lat: latitude coordinate
        :param float lng: longitude coordinate
        :param bool corners: return the lat and lng coordinates of the south-west
            and north-east corners of the what3words grid square.
        :param lang: response language
        :reference: http://developer.what3words.com/api/#positionto3
        :rtype: dict
        """

        params = {
            'position': '{0},{1}'.format(lat, lng),
            'corners': 'true' if corners else 'false',
            'lang': lang or self.lang,
        }

        return self._request('/position', params)

    def languages(self):
        """Retrieve a list of available 3 word languages.

        :reference: http://developer.what3words.com/api/#getlanguages
        :rtype: dict
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

