import requests
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()
# Endpoint URL for creating a client
create_url = 'http://127.0.0.1:8000/api/client/'

# JWT token for authentication
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc1NTc4LCJpYXQiOjE3MDQzNjk1NzgsImp0aSI6ImE3YjA0MjliOTVlNTQ2YzQ5ZjMwNmEwMTFmZjAwMzcwIiwidXNlcl9pZCI6M30.7ZzKeQHrnGm4WefA5olVU-9Pj2atcfcZoT6bnVNk3f4'

# Headers with JWT token
headers = {
    'Authorization': f'Bearer {jwt_token}'
}

# Client data to be created
client_data = {
    "full_name": "New Client",
    "email": "newclient@example.com",
    "phone" : "0215456897",
    "company_name" : "Tesla",
    "creation_date" :'2024-01-01',
    "last_update" :'2024-01-01',
    # ... other fields ...
}

# Make a POST request to create a client
response = requests.post(create_url, headers=headers, json=client_data)



if response.status_code in [200, 201]:
    client_created = response.json()
    console.print("Client created successfully.", style="bold green")
    
    # Using Rich for JSON formatting
    json_syntax = Syntax(str(client_created), "json", theme="monokai", line_numbers=True)
    console.print(json_syntax)
else:
    error_message = f"Failed to create client. Status code: {response.status_code} - {response.text}"
    console.print(error_message, style="bold red")
