import requests
from rich.console import Console
from rich import print as rprint
from datetime import datetime
from datetime import timedelta 
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')


console = Console()

create_event_url = 'http://127.0.0.1:8000/api/event/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'

headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type': 'application/json'
}


event_data = {
    "contract": 6,  
    "start_date": datetime.now().isoformat(),
    "end_date": (datetime.now() + timedelta(days=1)).isoformat(),
    "support_contact": 14, 
    "location": "Event Location",
    "attendees": 50,
    "notes": "Event notes"  
}


response = requests.post(create_event_url, headers=headers, json=event_data)

if response.status_code in [200, 201]:
    console.print("Event created successfully.", style="bold green")
    created_event = response.json()
    rprint(created_event)  
else:
    console.print(f"Failed to create event. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
