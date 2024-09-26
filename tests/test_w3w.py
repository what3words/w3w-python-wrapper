import unittest
import what3words
import json
from os import environ
from what3words import Geocoder, Coordinates, BoundingBox

# Setup environment variables for API key and addresses
api_key = environ.get('W3W_API_KEY', 'test_api_key')
addr = 'daring.lion.race'
lat = 51.508341
lng = -0.125499
suggest = 'index.home.rqft'
english = {'code': 'en', 'name': 'English', 'nativeName': 'English'}

class TestGeocoder(unittest.TestCase):

    def setUp(self):
        self.api_key = api_key
        self.geocoder = Geocoder(api_key=self.api_key)

    def test_convert_to_coordinates(self):
        # Test conversion to coordinates with a valid 3-word address
        result = self.geocoder.convert_to_coordinates(addr)
        if 'error' in result:
            print(f"API error code: {result['error']['code']}")
            # Handle the Quota Exceeded error specifically for this function
            self.assertEqual(result['error']['code'], 'QuotaExceeded', "Expected QuotaExceeded error for Convert to Coordinates")
        else:
            self.assertEqual(result['language'], 'en')
            self.assertEqual(result['coordinates']['lat'], lat)
            self.assertEqual(result['coordinates']['lng'], lng)

    def test_convert_to_3wa(self):
        # Test conversion of coordinates to a 3-word address
        result = self.geocoder.convert_to_3wa(Coordinates(lat, lng))
        if 'error' in result:
            print(f"API error code: {result['error']['code']}")
            # Handle the Quota Exceeded error specifically for this function
            self.assertEqual(result['error']['code'], 'QuotaExceeded', "Expected QuotaExceeded error for Convert to 3wa")
        else:
            self.assertEqual(result['language'], 'en')
            self.assertEqual(result['words'], 'daring.lion.race')
            self.assertEqual(result['coordinates']['lat'], lat)
            self.assertEqual(result['coordinates']['lng'], lng)

    def test_available_languages(self):
        # Test available languages
        result = self.geocoder.available_languages()
        self.assertIsNotNone(result['languages'])
        self.assertIn(english, result['languages'])

    def test_autosuggest(self):
        # Test autosuggest functionality with a partial word
        result = self.geocoder.autosuggest(suggest)
        self.assertGreater(len(result['suggestions']), 0, f"Expected suggestions for '{suggest}', but none were returned.")

    def test_grid_section(self):
        # Test grid section functionality with a bounding box
        sw = Coordinates(52.208867, 0.117540)
        ne = Coordinates(52.207988, 0.116126)
        bb = BoundingBox(sw, ne)

        result = self.geocoder.grid_section(bb)
        self.assertIsNotNone(result['lines'])

    def test_invalid_address(self):
        # Test invalid address
        invalid_addr = 'invalid.address.test'
        result = self.geocoder.convert_to_coordinates(invalid_addr)
        if 'error' in result:
            print(f"API error code: {result['error']['code']}")
            # Handle the Quota Exceeded error specifically for this function
            self.assertEqual(result['error']['code'], 'QuotaExceeded', "Expected QuotaExceeded error for Convert to 3wa")
        else:
            self.assertEqual(result['error']['code'], 'BadWords')

    def test_invalid_coordinates(self):
        # Test invalid coordinates to 3-word address conversion
        invalid_lat = 100.0
        invalid_lng = 200.0
        result = self.geocoder.convert_to_3wa(Coordinates(invalid_lat, invalid_lng))
        self.assertIn('error', result)
        self.assertEqual(result['error']['code'], 'BadCoordinates')

    def test_partial_autosuggest(self):
        # Test partial autosuggest functionality
        partial_suggest = 'daring.lion.r'
        result = self.geocoder.autosuggest(partial_suggest)
        print(json.dumps(result, indent=4))

        # Ensure the response contains the suggestions key
        self.assertIn('suggestions', result)

        # Check if there are valid suggestions
        self.assertGreater(len(result['suggestions']), 0, f"Expected suggestions for '{partial_suggest}', but none were returned.")

    def test_is_possible_3wa(self):
        # Test if a valid 3-word address is possible
        possible_3wa = 'index.home.raft'
        self.assertTrue(self.geocoder.is_possible_3wa(possible_3wa))
        invalid_3wa = 'index.home'
        self.assertFalse(self.geocoder.is_possible_3wa(invalid_3wa))

    def test_is_valid_3wa(self):
        # Test if a valid 3-word address is confirmed by the API
        valid_3wa = 'index.home.raft'
        self.assertTrue(self.geocoder.is_valid_3wa(valid_3wa))
        
        # Test an invalid 3-word address
        invalid_3wa = 'word.word.word'
        print(self.geocoder.is_valid_3wa(invalid_3wa))
        self.assertFalse(self.geocoder.is_valid_3wa(invalid_3wa))

    def test_find_possible_3wa(self):
        # Test finding possible 3-word addresses within a text
        text = "Here are some addresses: index.home.raft and index.home.shelf"
        result = self.geocoder.find_possible_3wa(text)
        self.assertIn('index.home.raft', result)
        self.assertIn('index.home.shelf', result)

    def test_did_you_mean(self):
        # Test 'did you mean' functionality with a near match
        near_miss = 'indx.home.rafe'
        self.assertTrue(self.geocoder.did_you_mean(near_miss))
        invalid_input = 'index.home'
        self.assertFalse(self.geocoder.did_you_mean(invalid_input))

if __name__ == '__main__':
    unittest.main()