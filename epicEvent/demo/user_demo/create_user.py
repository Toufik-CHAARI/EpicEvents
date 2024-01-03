import requests


create_user_url = 'http://127.0.0.1:8000/api-auth/users/create/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MjA3MTgwLCJpYXQiOjE3MDQyMDExODAsImp0aSI6IjIyNDNkMmNjMzBmMjQwMzZhMzBhYzhmYjNiZjFjOTE5IiwidXNlcl9pZCI6N30.VXBtj6h2H3SivDLJ9KsNioa9Kn4MifubOIJtJy3pIqs'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}

# User data to be created
user_data = {
    "username": "big.boss",
    "email": "newuser@example.com",
    "role": "management",  
    "password": "new_password"
}


response = requests.post(create_user_url, headers=headers, json=user_data)


if response.status_code in [200, 201]:
    print("User created successfully.")
    print(response.json())
else:
    print(f"Failed to create user. Status code: {response.status_code} - {response.text}")
