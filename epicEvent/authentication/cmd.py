import requests
from rich.table import Table
from rich.console import Console

# API URL
url = 'http://127.0.0.1:8000/api-auth/users'

# JWT token (replace with your actual token)
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMDA4Nzc5LCJpYXQiOjE3MDMwMDI3NzksImp0aSI6ImFmNjRmNTdlNDBjNTQ0MTg4ZDI1NDEwMzUwMWRlNWY5IiwidXNlcl9pZCI6Mn0.IvQ5To35apj6NRaCEBo5_3DM3Aqq7vkGnfYxzjSCwkQ'

# Headers with JWT token
headers = {
    'Authorization': f'Bearer {jwt_token}'
}

# Make a GET request to the API with the Authorization header
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    users = response.json()
    
    # Create a Rich table
    table = Table(title="User List")

    # Add columns (adjust based on your User model attributes)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Email", style="green")

    # Add rows to the table
    for user in users:
        table.add_row(str(user['id']), user['username'], user['email'])

    # Print the table to the console
    console = Console()
    console.print(table)
else:
    print(f"Failed to retrieve users. Status code: {response.status_code} - {response.text}")
