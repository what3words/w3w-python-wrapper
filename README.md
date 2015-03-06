w3w-python-wrapper
==================

Use the what3words API in your Python program (see http://developer.what3words.com/api)

## Functions

### getPosition(words=???)
This function takes the words parameter as either:
- a string of 3 words `'table.book.chair'`
- an array of 3 words `['table', 'book', 'chair']`

### getWords(lat=???, lng=???)
This function takes the latitude and longitude:
- 2 parameters:  `lat=0.1234`, `lng=1.5678`

## Code examples

### Get position
```python
w3w = what3words(apikey='YOURAPIKEY')
res = w3w.getPosition(words='prom.cape.pump')
print(res)
```

### Get 3 words
```python
w3w = what3words(apikey='YOURAPIKEY')
res = w3w.getWords(lat='51.484463', lng='-0.195405')
print(res)
```
