import requests


token_url = 'http://127.0.0.1:8000/api-auth/api/token/'  


credentials = {
    'username': 'big.boss',
    'password': 'new_password'
}


response = requests.post(token_url, data=credentials)


if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access']  
    print("Access Token:", access_token)
    # If you also need the refresh token
    refresh_token = token_data.get('refresh')  
    print("Refresh Token:", refresh_token)
else:
    print(f"Failed to obtain token. Status code: {response.status_code} - {response.text}")
