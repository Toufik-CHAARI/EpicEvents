import requests


delete_user_url = 'http://127.0.0.1:8000/api-auth/users/17/delete/' 


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MjA3MTgwLCJpYXQiOjE3MDQyMDExODAsImp0aSI6IjIyNDNkMmNjMzBmMjQwMzZhMzBhYzhmYjNiZjFjOTE5IiwidXNlcl9pZCI6N30.VXBtj6h2H3SivDLJ9KsNioa9Kn4MifubOIJtJy3pIqs'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.delete(delete_user_url, headers=headers)


if response.status_code in [200, 204]:  
    print("User deleted successfully.")
else:
    print(f"Failed to delete user. Status code: {response.status_code} - {response.text}")
