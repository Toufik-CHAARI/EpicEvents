import requests
from rich.console import Console
from rich.table import Table
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console = Console()


list_unsigned_contracts_url = 'http://127.0.0.1:8000/api/contracts/commercial/unsigned/'  


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc4NDU1LCJpYXQiOjE3MDQzNzI0NTUsImp0aSI6ImMyZjhkYmJmMWMyNDQxODFhNTU3YmQwYjliMTVjZTU0IiwidXNlcl9pZCI6M30.ZfPtoMqUUiHx3BF7pQV8cZVCCfVTYPqis7dUIiHHxI8'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.get(list_unsigned_contracts_url, headers=headers)

if response.status_code == 200:
    unsigned_contracts = response.json()
    
  
    table = Table(title="Unsigned Contracts for Commercial User")
    table.add_column("Contract ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Client ID", style="magenta")
    table.add_column("Total Amount", style="green")
    table.add_column("Remaining Amount", style="yellow")
    table.add_column("Creation Date", style="blue")

    
    for contract in unsigned_contracts:
        table.add_row(
            str(contract.get('id', 'N/A')),
            str(contract.get('client', 'N/A')),
            str(contract.get('total_amount', 'N/A')),
            str(contract.get('remaining_amount', 'N/A')),
            str(contract.get('creation_date', 'N/A'))
        )

    console.print(table)
else:
    console.print(f"Failed to retrieve unsigned contracts. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
