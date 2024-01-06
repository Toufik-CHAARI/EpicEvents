import requests
from rich.console import Console
from rich import print as rprint
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


update_contract_url = 'http://127.0.0.1:8000/api/contract/18/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'

headers = {
    'Authorization': f'Bearer {jwt_tokenM}',
    'Content-Type': 'application/json'
}


updated_data = {
    #"total_amount": 3333333,
    #"remaining_amount": 600.00,
    "is_signed": True,
    "sales_contact":22
   
}


response = requests.patch(update_contract_url, headers=headers, json=updated_data)  


if response.status_code == 200:
    console.print("Contract updated successfully.", style="bold green")
    updated_contract = response.json()
    rprint(updated_contract)  
else:
    console.print(f"Failed to update contract. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
