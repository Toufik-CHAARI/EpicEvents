import requests
from rich.console import Console
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


delete_contract_url = 'http://127.0.0.1:8000/api/contract/17/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'

headers = {
    'Authorization': f'Bearer {jwt_tokenC}'
}


response = requests.delete(delete_contract_url, headers=headers)

if response.status_code in [200, 204]:  
    console.print("Contract deleted successfully.", style="bold green")
else:
    console.print(f"Failed to delete contract. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
