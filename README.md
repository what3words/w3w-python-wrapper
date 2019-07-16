# <img src="https://what3words.com/assets/images/w3w_square_red.png" width="64" height="64" alt="what3words">&nbsp;w3w-python-wrapper [![Build Status](https://travis-ci.org/what3words/w3w-python-wrapper.svg?branch=master)](https://travis-ci.org/what3words/w3w-python-wrapper)

A Python library to use the [what3words REST API](https://docs.what3words.com/api/v3/).

Tested with Python 2.7, 3.4, 3.5, 3.6 (check travis-ci.org [build](https://travis-ci.org/what3words/w3w-python-wrapper/builds))

# Overview

The what3words Python library gives you programmatic access to 
* convert a 3 word address to coordinates 
* convert coordinates to a 3 word address
* autosuggest functionality which takes a slightly incorrect 3 word address, and suggests a list of valid 3 word addresses
* obtain a section of the 3m x 3m what3words grid for a bounding box.
* determine the currently support 3 word address languages.

## Authentication

To use this library you’ll need a what3words API key, which can be signed up for [here](https://accounts.what3words.com/).

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

## Convert To Coordinates

This function takes the words parameter as a string of 3 words `'table.book.chair'`

The returned payload from the `convert-to-coordinates` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v3/#convert-to-coordinates).

## Convert To 3 Word Address

This function takes the latitude and longitude:
- 2 parameters:  `lat=0.1234`, `lng=1.5678`

The returned payload from the `convert-to-3wa` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v3/#convert-to-3wa).


## AutoSuggest

Returns a list of 3 word addresses based on user input and other parameters.

This method provides corrections for the following types of input error:
* typing errors
* spelling errors
* misremembered words (e.g. singular vs. plural)
* words in the wrong order

The `autosuggest` method determines possible corrections to the supplied 3 word address string based on the probability of the input errors listed above and returns a ranked list of suggestions. This method can also take into consideration the geographic proximity of possible corrections to a given location to further improve the suggestions returned.

### Input 3 word address

You will only receive results back if the partial 3 word address string you submit contains the first two words and at least the first character of the third word; otherwise an error message will be returned.

### Clipping and Focus

We provide various `clip` policies to allow you to specify a geographic area that is used to exclude results that are not likely to be relevant to your users. We recommend that you use the `clip` parameter to give a more targeted, shorter set of results to your user. If you know your user’s current location, we also strongly recommend that you use the `focus` to return results which are likely to be more relevant.

In summary, the `clip` policy is used to optionally restrict the list of candidate AutoSuggest results, after which, if focus has been supplied, this will be used to rank the results in order of relevancy to the focus.

https://docs.what3words.com/api/v3/#autosuggest

The returned payload from the `autosuggest` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v3/#autosuggest).

## Grid Section

Returns a section of the 3m x 3m what3words grid for a bounding box.

## Available Languages

Retrieves a list of the currently loaded and available 3 word address languages.

The returned payload from the `available-languages` method is described in the [what3words REST API documentation](https://docs.what3words.com/api/v3/#available-languages).

## Code examples

### W3W-API-KEY
For safe storage of your API key on your computer, you can define that API key using your system’s environment variables.
```bash
$ export W3W_API_KEY=<Secret API Key>
```

### Convert to coordinates
```python
import what3words
from os import environ
api_key = environ['W3W_API_KEY']
w3w = what3words.Geocoder(api_key)
res = w3w.convert_to_coordinates('prom.cape.pump')
print(res)
```

### Convert to 3 word address
```python
import what3words
from os import environ
api_key = environ['W3W_API_KEY']
w3w = what3words.Geocoder(api_key)
res = w3w.convert_to_3wa(what3words.Coordinates(51.484463,-0.195405))
print(res)
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

* `v3.0.2`  16/07/19 - Include User-Agent in API requests
* `v3.0.0`  04/02/19 - Updated wrapper to use what3words API v3
* `v2.2.1`  08/09/17 - Python 3 setup install fixed thanks to [@joedborg](https://github.com/joedborg)
* `v2.2.0`  07/09/17 - Python 3 support, thanks to [@joedborg](https://github.com/joedborg)
* `v2.1.1`  07/09/17 - update README : this library is compatible with Python 2
* `v2.1.0`  28/03/17 - Added multilingual version of `autosuggest` and `standardblend`
* `v2.0.2`  27/10/16 - Published on PyPi
* `v2.0.0`  10/06/16 - Updated wrapper to use what3words API v2

## Licensing

The MIT License (MIT)

A copy of the license is available in the repository's [license](LICENSE) file.
