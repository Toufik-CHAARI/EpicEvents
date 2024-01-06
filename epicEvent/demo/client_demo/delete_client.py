import requests
from rich.console import Console
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


delete_event_url = 'http://127.0.0.1:8000/api/client/20/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0MzkxODcyLCJpYXQiOjE3MDQzNzc0NzIsImp0aSI6IjkzM2Q4NmUxNzc3ODQ1OWI5NWQ2YzMxMThjZTU3YTMxIiwidXNlcl9pZCI6MTR9.fxDIkh6AnsxT2BsouV3EgvFvSKKwxEZtD9RZzVi3nnY'

headers = {
    'Authorization': f'Bearer {jwt_tokenM}'
}


response = requests.delete(delete_event_url, headers=headers)

if response.status_code in [200, 204]:  
    console.print("Client deleted successfully.", style="bold green")
else:
    console.print(f"Failed to delete Client. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
