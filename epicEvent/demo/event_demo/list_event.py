import requests
from rich.console import Console
from rich.table import Table
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

# Initialize Rich console
console = Console()

# Endpoint URL for listing events
list_events_url = 'http://127.0.0.1:8000/api/event/'  

# JWT token for authentication
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'

# Headers with JWT token
headers = {
    'Authorization': f'Bearer {jwt_token}'
}

# Make a GET request to list events
response = requests.get(list_events_url, headers=headers)

if response.status_code == 200:
    events = response.json()
    
    # Create a Rich table
    table = Table(title="Event List")
    table.add_column("Event ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Contract ID", style="magenta")
    table.add_column("Start Date", style="green")
    table.add_column("End Date", style="yellow")
    table.add_column("Support Contact", style="blue")
    table.add_column("Location", style="red")
    table.add_column("Attendees", style="purple")

    for event in events:
        support_contact = str(event.get('support_contact', 'N/A'))  
        contract_id = str(event.get('contract', 'N/A'))  
        table.add_row(
            str(event.get('id', 'N/A')),
            contract_id,
            str(event.get('start_date', 'N/A')),
            str(event.get('end_date', 'N/A')),
            support_contact,
            str(event.get('location', 'N/A')),
            str(event.get('attendees', 'N/A'))
        )

    console.print(table)
else:
    console.print(f"Failed to retrieve events. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
