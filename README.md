# ![what3words](https://map.what3words.com/images/map/marker-border.png)w3w-python-wrapper

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

## Functions

### position(words=???)
This function takes the words parameter as either:
- a string of 3 words `'table.book.chair'`
- an array of 3 words `['table', 'book', 'chair']`

### words(lat=???, lng=???)
This function takes the latitude and longitude:
- 2 parameters:  `lat=0.1234`, `lng=1.5678`

### langauges()
This function returns all available languages

## Code examples

### Forward Geocode
```python
>>> import what3words
>>> w3w = what3words.Geocoder(api_key='YOUR-API-KEY')
>>> res = w3w.position(words='prom.cape.pump')
>>> print(res)
```

### Reverse Geocode
```python
>>> import what3words
>>> w3w = what3words.Geocoder(api_key='YOUR-API-KEY')
>>> res = w3w.words(lat='51.484463', lng='-0.195405')
>>> print(res)
```
