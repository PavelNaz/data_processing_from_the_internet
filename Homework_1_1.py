import requests
import json

url = 'https://api.github.com'
user = 'PavelNaz'

response = requests.get(f'{url}/users/{user}/repos')


with open('data.json', 'w') as f:
    json.dump(response.json(), f)

for x in response.json():
    print(x['name'])