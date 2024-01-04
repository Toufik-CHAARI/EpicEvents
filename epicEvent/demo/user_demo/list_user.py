import requests
from rich.table import Table
from rich.console import Console
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')

url = 'http://127.0.0.1:8000/api-auth/users'


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzcxMzY4LCJpYXQiOjE3MDQzNjUzNjgsImp0aSI6ImE5MTkzMTdmOGVhMDRhZjliMTkxM2M0NDcxZWNhYzdhIiwidXNlcl9pZCI6MTh9.N2f9qfIvtljhehhejTSa5bPZl0evUHjCvqphQGkmfW0'


headers = {
    'Authorization': f'Bearer {jwt_tokenM}'
}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    users = response.json()
    
    
    table = Table(title="User List")

    
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Role", style="green")

    
    for user in users:
        table.add_row(str(user['id']), user['username'], user['email'],user['role'])

   
    console = Console()
    console.print(table)
else:
    print(f"Failed to retrieve users. Status code: {response.status_code} - {response.text}")
