import requests

print(requests.get('http://localhost:5000/api/getusers').json()[0]['id'])