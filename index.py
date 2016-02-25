from __future__ import division
import urllib2, json, os.path
import json, time
import requests
import logging

if os.path.exists('config/config-local.json'):
    config_file = open('config/config-local.json')
    config = json.load(config_file)
else:
    print 'Please copy the config.json file to config-local.json and fill in the file.'
logging.basicConfig(filename='eagle.log',level=logging.DEBUG)


logging.info(time.strftime("%x") + ": eagle woke up")

def sendMail(amount, lastPrice):
    r = requests.post(
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



try:
    price = config['currencies']['BTC']['balance']
except:
    try:
        html = urllib2.urlopen('https://blockchain.info/q/addressbalance/' + config['currencies']['BTC']['address'])
        price = int(html.read()) /  pow(10, 8) #satoshi to BTC convertion
    except:
        price = 0

for currency in config['currencies'].keys():
    if currency != 'BTC':
        html = urllib2.urlopen('https://bittrex.com/api/v1.1/public/getticker?market=BTC-' + currency)
        res = json.loads(html.read())['result']
        price += res['Bid'] * config['currencies'][currency]['balance']


res = urllib2.urlopen('https://blockchain.info/ticker')
lastPrice = json.loads(res.read())['EUR']['last']

logging.info("Total bitcoins if converted: " + str(price) + " BTC.\r\nThis equals to " + str(price * lastPrice) + " euro.")

if (sendMail(price, lastPrice)):
    logging.info("Email sent")
else:
    logging.error("An error occured on email send")
