import urllib2, json, os.path
import json

if os.path.exists('config/config-local.json'):
    config_file = open('config/config-local.json')
else:
    print 'Please copy the config.json file to config-local.json and fill in the file.'

currencies = json.load(config_file)

if currencies['BTC'] is not None:
    price = currencies['BTC']
else:
    price = 0

for currency in currencies.keys():
    if currency != 'BTC':
        html = urllib2.urlopen('https://bittrex.com/api/v1.1/public/getticker?market=BTC-' + currency)
        res = json.loads(html.read())['result']
        price += res['Bid'] * currencies[currency]

res = urllib2.urlopen('https://blockchain.info/ticker')
lastPrice = json.loads(res.read())['EUR']['last']

print "If you sell everything you have right now with the bid price you would have in total", price, "BTC."
print "This equals to", price * lastPrice, "euro."
