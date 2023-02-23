import requests

# response = requests.post('http://127.0.0.1:5000/users',
#                          json={'username': 'user-6', 'password': '2345'})

response = requests.delete('http://127.0.0.1:5000/users/22')

print(response.status_code)
print(response.json())

response = requests.get('http://127.0.0.1:5000/users/22')

print(response.status_code)
print(response.json())