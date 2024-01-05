import requests
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')


console= Console()



update_url = 'http://127.0.0.1:8000/api/client/18/'


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc1NTc4LCJpYXQiOjE3MDQzNjk1NzgsImp0aSI6ImE3YjA0MjliOTVlNTQ2YzQ5ZjMwNmEwMTFmZjAwMzcwIiwidXNlcl9pZCI6M30.7ZzKeQHrnGm4WefA5olVU-9Pj2atcfcZoT6bnVNk3f4'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}




updated_data = {
    "full_name": "Old Client",
    
}


response = requests.patch(update_url, headers=headers, json=updated_data)



if response.status_code == 200:
    print("Client updated successfully.")
else:
    print(f"Failed to update client. Status code: {response.status_code} - {response.text}")


if response.status_code in [200, 201]:
    client_updated = response.json()
    console.print("Client updated successfully.", style="bold green")
    
    
    json_syntax = Syntax(str(client_updated), "json", theme="monokai", line_numbers=True)
    console.print(json_syntax)
else:
    error_message = f"Failed to update client. Status code: {response.status_code} - {response.text}"
    console.print(error_message, style="bold red")