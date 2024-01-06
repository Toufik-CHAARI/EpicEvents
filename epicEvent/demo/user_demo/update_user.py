import requests
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

update_user_url = 'http://127.0.0.1:8000/api-auth/users/23/update/'  


jwt_token = 'your_jwt_token'


headers = {
    'Authorization': f'Bearer {jwt_tokenS}'
}


updated_data = {
    "username": "updatedusername",
    "email": "updatedemail@example.com",
    
}


response = requests.patch(update_user_url, headers=headers, json=updated_data)  # For a full update
# response = requests.patch(update_user_url, headers=headers, json=updated_data)  # For a partial update


if response.status_code == 200:
    print("User updated successfully.")
    print(response.json())
else:
    print(f"Failed to update user. Status code: {response.status_code} - {response.text}")
