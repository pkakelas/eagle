from __future__ import division
import urllib.request as request, json, os.path
import json, time


if os.path.exists('config/config.json'):
    config_file = open('config/config.json')
    config = json.load(config_file)
else:
    print('Please copy the config.json file to config-local.json and fill in the file.')
    exit()

print(time.strftime("%x") + ": Eagle woke up")

def sendMail(amount, lastPrice):

    r = request.post(
        "https://api.mailgun.net/v3/sandboxb0290be0c6374214b94158e8986a61b2.mailgun.org/messages",
        auth=("api", "key-7f1ccf639b43e107cda773f9eec84ea5"),
        data={"from": "Eagle <postmaster@sandboxb0290be0c6374214b94158e8986a61b2.mailgun.org>",
              "to": config['myName'] + " <" + config['myMail'] + ">",
              "subject": "Crypto finance report",
              "text": "Good evening Mitsara,\r\n\r\nIf you sell everything you have right now with the bid price you would have in total " + str(amount) + "BTC. \r\nThis equals to " + str(amount * lastPrice) + " euro. \r\n\r\nHave a beautiful day,\r\nEagle"})

    if (r.status_code) == 200:
        return True
    else:
        return False

total_volume = 0
lastPrice = 0
symbols = ','.join(config['currencies'])
url = "http://api.coinlayer.com/api/live?access_key=" + config['coinlayer'] + "&target=EUR&symbols=" + symbols

with request.urlopen(url) as response:
   rates = json.loads(response.read().decode('utf-8')).get('rates')

   for currency in config['currencies'].keys():
       lastPrice = rates.get(currency)

       if lastPrice == None:
           print("This cryptocurrency does not exist")
           continue

       total_volume += lastPrice * config['currencies'][currency]['balance']

print("Total euro : " + str(total_volume) + " eur")

if (sendMail(total_volume, lastPrice)):
    print("Email sent")
else:
    print("An error occured on email send")
