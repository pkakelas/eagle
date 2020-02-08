from __future__ import division
import urllib.request as request, json, os.path
import json, time


if os.path.exists('config/config.json'):
    config_file = open('config/config.json')
    config = json.load(config_file)
else:
    print('Please copy the config.json.template file to config.json and fill in the file.')
    exit()

print(time.strftime("%x") + ": Eagle woke up")

total_volume = 0
symbols = ','.join(config['currencies'])
url = "http://api.coinlayer.com/api/live?access_key=" + config['coinlayer'] + "&target=EUR&symbols=" + symbols

with request.urlopen(url) as response:
   rates = json.loads(response.read().decode('utf-8'))['rates']

   for currency in config['currencies'].keys():
       if currency not in rates:
           print("Cryptocurrency", currency, "does not exist.")
           continue

       total_volume += rates[currency] * config['currencies'][currency]['balance']

print("Total euro : " + str(total_volume) + " eur")
