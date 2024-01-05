import requests
from rich.table import Table
from rich.console import Console
import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')

console=Console()

url = 'http://127.0.0.1:8000/api/contract/'


jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzc3OTMwLCJpYXQiOjE3MDQzNzE5MzAsImp0aSI6ImE2ZjIxNDBhZDRjMTQxNmI4ZTU1MGRkMmU5YWZjZGE1IiwidXNlcl9pZCI6N30.ZzIEYg0OC5wyG66Xx0qLCheFTwmkbht5JLLlPjTvF8A'


headers = {
    'Authorization': f'Bearer {jwt_token}'
}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    contracts = response.json()
    
    # Create a Rich table
    table = Table(title="Contract List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Client ID", style="magenta")
    table.add_column("Total Amount", style="green")
    table.add_column("Remaining Amount", style="yellow")
    table.add_column("Creation Date", style="blue")
    table.add_column("Is Signed", style="red")
    table.add_column("sales_contact", style="red")
    
    
    for contract in contracts:
        is_signed = "Yes" if contract.get('is_signed', False) else "No"
        table.add_row(
            str(contract.get('id', 'N/A')),
            str(contract.get('client', {})),
            str(contract.get('total_amount', 'N/A')),
            str(contract.get('remaining_amount', 'N/A')),
            str(contract.get('creation_date', 'N/A')),
            is_signed,
            str(contract.get('sales_contact', 'N/A')),
        )

    console = Console()
    console.print(table)
else:
    print(f"Failed to retrieve contracts. Status code: {response.status_code} - {response.text}")