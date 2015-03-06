import urllib
import urllib2
import json

class what3words(object):
    """what3words API"""

    def __init__(self, host='api.what3words.com', apikey=''):
        self.host = 'http://' + host
        self.apikey = apikey

    def getPosition(self, words='*libertytech', onewordpassword='',
                    lang='en', corners='false', email='', password=''):
        if isinstance(words, list):
            words = "%s.%s.%s" % (words[0], words[1], words[2])
            print "string is: %s" % (words)
        params = { 'corners': corners, 'string': words }
        if (onewordpassword != ''):
            params.update({'onewordpassword', onewordpassword,
                           'email', email,
                           'password', password});
        return self.postRequest(self.host + '/w3w', params)

    def getWords(self, lat='', lng='', corners='false', lang='en'):
        position = "%s,%s" % (lat, lng)
        params = { 'position': position, 'corners': corners, 'lang': lang }
        return self.postRequest(self.host + '/position', params)

    def getLanguages(self):
        return self.postRequest(self.host + '/get-languages', dict())

    def postRequest(self, url, params):
        params.update({'key': self.apikey})
        encparams = urllib.urlencode(params)
        try: response = urllib.urlopen(url, encparams).read()
        except URLError as e:
            raise e
        return json.loads(response)
