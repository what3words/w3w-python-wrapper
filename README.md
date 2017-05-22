# <img src="https://what3words.com/assets/images/w3w_square_red.png" width="64" height="64" alt="what3words">&nbsp;w3w-python-wrapper ![Build Status](https://travis-ci.org/what3words/w3w-python-wrapper.svg?branch=master)

A Python library to use the [what3words REST API](https://docs.what3words.com/api/v2/).

# Overview

The what3words Python library gives you programmatic access to convert a 3 word address to coordinates (_forward geocoding_), to convert coordinates to a 3 word address (_reverse geocoding_), and to determine the currently support 3 word address languages.

## Authentication

To use this library you’ll need a what3words API key, which can be signed up for [here](https://map.what3words.com/register?dev=true).

# Installation

## PyPi Install

To install what3words, simply:

```bash
$ pip install what3words
```

## GitHub Install

Installing the latest version from Github:

```bash
$ git clone https://github.com/what3words/w3w-python-wrapper.git
$ cd w3w-python-wrapper
$ python setup.py install
```

## Forward geocoding
Forward geocodes a 3 word address to a position, expressed as coordinates of latitude and longitude.

This function takes the words parameter as a string of 3 words `'table.book.chair'`

The returned payload from the `forwardGeocode` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v2/#forward-result).

## Reverse geocoding

Reverse geocodes coordinates, expressed as latitude and longitude to a 3 word address.

This function takes the latitude and longitude:
- 2 parameters:  `lat=0.1234`, `lng=1.5678`

The returned payload from the `reverseGeocode` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v2/#reverse-result).


## AutoSuggest

Returns a list of 3 word addresses based on user input and other parameters.

This method provides corrections for the following types of input error:
* typing errors
* spelling errors
* misremembered words (e.g. singular vs. plural)
* words in the wrong order

The `autoSuggest` method determines possible corrections to the supplied 3 word address string based on the probability of the input errors listed above and returns a ranked list of suggestions. This method can also take into consideration the geographic proximity of possible corrections to a given location to further improve the suggestions returned.

### Single and Multilingual Variants
AutoSuggest is provided via 2 variant resources; single language and multilingual.

The single language autosuggest resource requires a language to be specified. The input full or partial 3 word address will be interpreted as being in the specified language and all suggestions will be in this language. We recommend that you set this according to the language of your user interface, or the browser/device language of your user. If your software or app displays 3 word addresses to users (in addition to accepting 3 words as a search/input) then we recommend you set the language parameter for this resource to the same language that 3 word addresses are displayed to your users.

The multilingual `autosuggest-ml` resource can accept an optional language. If specified, this will ensure that the `autosuggest-ml` resource will look for suggestions in this language, in addition to any other languages that yield relevant suggestions.

### Input 3 word address

You will only receive results back if the partial 3 word address string you submit contains the first two words and at least the first character of the third word; otherwise an error message will be returned.

### Clipping and Focus

We provide various `clip` policies to allow you to specify a geographic area that is used to exclude results that are not likely to be relevant to your users. We recommend that you use the `clip` parameter to give a more targeted, shorter set of results to your user. If you know your user’s current location, we also strongly recommend that you use the `focus` to return results which are likely to be more relevant.

In summary, the `clip` policy is used to optionally restrict the list of candidate AutoSuggest results, after which, if focus has been supplied, this will be used to rank the results in order of relevancy to the focus.

http://docs.what3words.local/api/v2/#autosuggest-clip

The returned payload from the `autoSuggest` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v2/#autosuggest-result).

## Standardblend
Returns a blend of the three most relevant 3 word address candidates for a given location, based on a full or partial 3 word address.

The specified 3 word address may either be a full 3 word address or a partial 3 word address containing the first 2 words in full and at least 1 character of the 3rd word. The standardblend resource provides the search logic that powers the search box on map.what3words.com and in the what3words mobile apps.

*Single and Multilingual Variants*

AutoSuggest is provided via 2 variant resources; single language and multilingual.

The single language `standardblend` method requires a language to be specified.

The multilingual `standardblend_ml` method requires a language to be specified. This will ensure that the standardblend-ml resource will look for suggestions in this language, in addition to any other languages that yield relevant suggestions.

see https://docs.what3words.com/api/v2/#standardblend for detailed information


## Get Languages

Retrieves a list of the currently loaded and available 3 word address languages.

The returned payload from the `languages` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v2/#lang-result).

## Code examples

### W3W-API-KEY
For safe storage of your API key on your computer, you can define that API key using your system’s environment variables.
```bash
$ export W3W_API_KEY=<Secret API Key>
```

### Forward Geocode
```python
>>> import what3words
>>> from os import environ
>>> api_key = environ['W3W_API_KEY']
>>> w3w = what3words.Geocoder(api_key)
>>> res = w3w.forward(addr='prom.cape.pump')
>>> print(res)
```

### Reverse Geocode
```python
>>> import what3words
>>> from os import environ
>>> api_key = environ['W3W_API_KEY']
>>> w3w = what3words.Geocoder(api_key)
>>> res = w3w.reverse(lat=51.484463, lng=-0.195405)
>>> print(res)
```

## Issues

Find a bug or want to request a new feature? Please let us know by submitting an issue.

## Contributing
Anyone and everyone is welcome to contribute.

1. Fork it (https://github.com/what3words/w3w-python-wrapper and click "Fork")
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


# Revision History

* `v2.1.0`  28/03/17 - Added multilingual version of `autosuggest` and `standardblend`
* `v2.0.2`  27/10/16 - Pusblished on PyPi
* `v2.0.0`  10/06/16 - Updated wrapper to use what3words API v2

## Licensing

The MIT License (MIT)

A copy of the license is available in the repository's [license](LICENSE) file.
