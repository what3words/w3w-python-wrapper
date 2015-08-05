w3w-python-wrapper
==================

Use the what3words API in your Python program (see http://developer.what3words.com/api)

## Functions

### position(words=???)
This function takes the words parameter as either:
- a string of 3 words `'table.book.chair'`
- an array of 3 words `['table', 'book', 'chair']`

### words(lat=???, lng=???)
This function takes the latitude and longitude:
- 2 parameters:  `lat=0.1234`, `lng=1.5678`

## Code examples

```from what3words import What3Words```

### Get position
```python
w3w = What3Words(api_key='YOURAPIKEY')
res = w3w.position(words='prom.cape.pump')
print(res)
```

### Get 3 words
```python
w3w = what3words(api_key='YOURAPIKEY')
res = w3w.words(lat='51.484463', lng='-0.195405')
print(res)
```
