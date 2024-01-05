import requests
from rich.console import Console
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()

delete_user_url = 'http://127.0.0.1:8000/api-auth/users/19/delete/' 


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzcxMzY4LCJpYXQiOjE3MDQzNjUzNjgsImp0aSI6ImE5MTkzMTdmOGVhMDRhZjliMTkxM2M0NDcxZWNhYzdhIiwidXNlcl9pZCI6MTh9.N2f9qfIvtljhehhejTSa5bPZl0evUHjCvqphQGkmfW0'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.delete(delete_user_url, headers=headers)


if response.status_code in [200, 204]:
    console.print("User deleted successfully.", style="bold green")
else:
    error_message = f"Failed to delete user. Status code: {response.status_code} - {response.text}"
    console.print(error_message, style="bold red")
