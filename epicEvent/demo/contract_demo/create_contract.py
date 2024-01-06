import requests
from rich.console import Console
from rich import print as rprint
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()

create_contract_url = 'http://127.0.0.1:8000/api/contract/'  

jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'

headers = {
    'Authorization': f'Bearer {jwt_tokenM}',
    'Content-Type': 'application/json'
}


contract_data = {
    "client": 19,  
    "sales_contact": 22,  
    "total_amount": 11230.00,
    "remaining_amount": 500.00,
    "creation_date": "2023-01-01",
    "is_signed": False
}


response = requests.post(create_contract_url, headers=headers, json=contract_data)

if response.status_code in [200, 201]:
    console.print("Contract created successfully.", style="bold green")
    created_contract = response.json()
    rprint(created_contract)  
else:
    console.print(f"Failed to create contract. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
