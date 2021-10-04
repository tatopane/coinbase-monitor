import requests as r
import os
from datetime import datetime, timedelta
import json
from pushbullet import Pushbullet
from decouple import config

test = False

with open('settings.json', 'r') as f:
    settings = json.load(f)

pb = Pushbullet(config('PUSHBULLET_API_KEY'))
if not pb:
	raise("Couldn't initialize Pushbullet")
	exit()

for cur in settings.keys():
	if settings[cur]['bounds']:
		last_alert = settings[cur]["last_alert"] if "last_alert" in settings[cur] else None
		url = 'https://api.coinbase.com/v2/prices/{}-USD/spot'.format(cur)
		price = float(r.get(url).json()['data']['amount'])

		if test or (settings[cur]['bounds'][0] and price <= settings[cur]['bounds'][0]):
			print(cur, price, ' lower than ', settings[cur]['bounds'][0])
			if test or (last_alert and datetime.now()-timedelta(hours=24) <= last_alert):
				print(cur,'should notify', last_alert)
				settings[cur]['last_alert'] = str(datetime.now())
				push = pb.push_note("Crypto Alert: Time to buy", "{} trading at {} (below {})".format(cur,price,settings[cur]['bounds'][0]))

		elif settings[cur]['bounds'][1] and price >= settings[cur]['bounds'][1]:
			print(cur, price, ' higher than ', settings[cur]['bounds'][1])
			if test or (last_alert and datetime.now()-timedelta(hours=24) <= last_alert):
				print(cur,'should notify', last_alert)
				settings[cur]['last_alert'] = str(datetime.now())
				push = pb.push_note("Crypto Alert: Time to sell", "{} trading at {} (above {})".format(cur,price,settings[cur]['bounds'][0]))

		else:
			print(cur, price)

#write it back to the file
with open('settings.json', 'w') as f:
    json.dump(settings, f)

##https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file




