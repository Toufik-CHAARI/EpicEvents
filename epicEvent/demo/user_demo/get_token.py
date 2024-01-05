import requests
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

token_url = 'http://127.0.0.1:8000/api-auth/api/token/'  

'''
credentials = {
    'username': 'big.boss',
    'password': 'new_password'
}
'''
'''
credentials = {
    'username': 'laeticia.casta',
    'password': 'moi123'
}
'''

credentials = {
    'username': 'Linda.desuza',
    'password': 'moi123'
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
