import requests

# response = requests.post('http://127.0.0.1:5000/users',
#                          json={'username': 'user-9', 'password': '2345'})

response = requests.get('http://127.0.0.1:5000/users/1')

print(response.status_code)
print(response.json())