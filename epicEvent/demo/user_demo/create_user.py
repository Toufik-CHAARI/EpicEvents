import requests
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint

console = Console()
create_user_url = 'http://127.0.0.1:8000/api-auth/users/create/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzcxMzY4LCJpYXQiOjE3MDQzNjUzNjgsImp0aSI6ImE5MTkzMTdmOGVhMDRhZjliMTkxM2M0NDcxZWNhYzdhIiwidXNlcl9pZCI6MTh9.N2f9qfIvtljhehhejTSa5bPZl0evUHjCvqphQGkmfW0'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}

# User data to be created
user_data = {
    "username": "big.lewoski",
    "email": "newuser@example.com",
    "role": "management",  
    "password": "new_password"
}


response = requests.post(create_user_url, headers=headers, json=user_data)


if response.status_code in [200, 201]:
    user_created = response.json()
    console.print("User created successfully.", style="bold green")
    
    # Using Rich for JSON formatting
    json_syntax = Syntax(str(user_created), "json", theme="monokai", line_numbers=True)
    console.print(json_syntax)
else:
    error_message = f"Failed to create user. Status code: {response.status_code} - {response.text}"
    console.print(error_message, style="bold red")
