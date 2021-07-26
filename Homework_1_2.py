import requests
import json

service = 'https://samples.openweathermap.org/data/2.5/weather'
appid = ' dce4eaf2ff722be418f733012656c22a'
city = 'London'

response1 = requests.get(f'{service}?q={city}&appid={appid}')
response1.json()

print(response1)

with open('response1.json', 'w') as f:
    json.dump(response1.json(), f)
