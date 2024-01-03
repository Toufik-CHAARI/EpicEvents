import requests
from rich.table import Table
from rich.console import Console


url = 'http://127.0.0.1:8000/api-auth/users'


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MjE3NTE2LCJpYXQiOjE3MDQyMTE1MTYsImp0aSI6IjZhNmJkNDgxN2U0NzQyZTdiNjU2NmEwOGQzOWQ4OGQ5IiwidXNlcl9pZCI6MTh9.ubv2LuQxDRDvGtah84TGVVDGBhcn8mu1vdEfaKMFZGY'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    users = response.json()
    
    
    table = Table(title="User List")

    
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")

    
    for user in users:
        table.add_row(str(user['id']), user['username'], user['email'])

   
    console = Console()
    console.print(table)
else:
    print(f"Failed to retrieve users. Status code: {response.status_code} - {response.text}")
