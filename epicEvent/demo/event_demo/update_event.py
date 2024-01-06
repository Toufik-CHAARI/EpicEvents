import requests
from rich.console import Console
from rich import print as rprint
from datetime import datetime
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


update_event_url = 'http://127.0.0.1:8000/api/event/19/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzkxODcyLCJpYXQiOjE3MDQzNzc0NzIsImp0aSI6IjkzM2Q4NmUxNzc3ODQ1OWI5NWQ2YzMxMThjZTU3YTMxIiwidXNlcl9pZCI6MTR9.fxDIkh6AnsxT2BsouV3EgvFvSKKwxEZtD9RZzVi3nnY'

headers = {
    'Authorization': f'Bearer {jwt_tokenM}',
    'Content-Type': 'application/json'
}


updated_data = {    
    #"location": "MIAMI",
    #"attendees": 100,
    #"notes": "Updated event notes"  
    "support_contact": 25, 
}


response = requests.patch(update_event_url, headers=headers, json=updated_data)  


if response.status_code == 200:
    console.print("Event updated successfully.", style="bold green")
    updated_event = response.json()
    rprint(updated_event)  
else:
    console.print(f"Failed to update event. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
