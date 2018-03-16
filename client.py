import json
import requests

payload = {'mode': 'classify', 'data': 'http://www.yahoo.co.jp'}

r = requests.post('http://localhost:11000/classify', data=json.dumps(payload) )

print(  r.text )

payload = {'mode': 'classify', 'data': 'http://wwwqwwwwwww.yahoo.co.jp'}
r = requests.post('http://localhost:11000/classify', data=json.dumps(payload) )

print(  r.text )
