import requests
from rich.console import Console
from rich.table import Table
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


list_null_support_events_url = 'http://127.0.0.1:8000/api/null-role-events/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzkyNDYxLCJpYXQiOjE3MDQzNzgwNjEsImp0aSI6IjM5NWU5M2JhM2ZlYTRkNGQ5NDc0OTM5ZGQ5ZGQ3ZDFiIiwidXNlcl9pZCI6N30.ZK63VaVp9qeFR1OJcESgTl3_tDvip-owtQgAaWEpN7A'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.get(list_null_support_events_url, headers=headers)

if response.status_code == 200:
    events = response.json()
    
    # Create a Rich table
    table = Table(title="Events Without Assigned Support Contact")
    table.add_column("Event ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Contract ID", style="magenta")
    table.add_column("Start Date", style="green")
    table.add_column("End Date", style="yellow")
    table.add_column("Location", style="blue")
    table.add_column("Attendees", style="red")
    table.add_column("Support", style="red")

    
    for event in events:
        table.add_row(
            str(event.get('id', 'N/A')),
            str(event.get('contract', 'N/A')),  
            str(event.get('start_date', 'N/A')),
            str(event.get('end_date', 'N/A')),
            str(event.get('location', 'N/A')),
            str(event.get('attendees', 'N/A')),
            str(event.get('support_contact', 'N/A'))
        )

    console.print(table)
else:
    console.print(f"Failed to retrieve events. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
