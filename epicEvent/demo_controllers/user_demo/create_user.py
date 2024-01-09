import requests
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')


console = Console()
create_user_url = 'http://127.0.0.1:8000/api-auth/users/create/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NTU2NzQxLCJpYXQiOjE3MDQ1NDIzNDEsImp0aSI6IjIwNjcyOWU4N2JmYTRjYjU4NTE0MmFkZTgxMTU3ZGU5IiwidXNlcl9pZCI6Mn0.jSZ6TVqnijHCDSwErEfLRAfSbQDZ1O0rU7AExe4JKik'


headers = {
    'Authorization': f'Bearer {jwt_tokenM}'
}

# User data to be created
user_data = {
    "username": "francis.lalane",
    "email": "newuser@example.com",
    "role": "support",  
    "password": "moi123"
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
