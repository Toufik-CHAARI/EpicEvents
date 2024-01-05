import requests
from rich.table import Table
from rich.console import Console

import os


jwt_tokenM = os.getenv('jwt_tokenM')
jwt_tokenC = os.getenv('jwt_tokenC')
jwt_tokenS = os.getenv('jwt_tokenS')





list_url = 'http://127.0.0.1:8000/api/client'


#jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0Mzk2Mjg1LCJpYXQiOjE3MDQzODE4ODUsImp0aSI6Ijk2YWY0Njk5MWRmZDQ0OGJiYWFkMWM1MTg2OThhMzFlIiwidXNlcl9pZCI6N30.7R5IL02WorY1k6un5HElZWguBD_xcw7inwJxilZKtjA'


headers = {
    'Authorization': f'Bearer {jwt_tokenM}'
}


response = requests.get(list_url, headers=headers)

if response.status_code == 200:
    clients = response.json()
    
    
    table = Table(title="Client List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Company Name", style="yellow")
    table.add_column("Sales Contact", style="blue")
    

    
    for client in clients:
        sales_contact = str(client.get('sales_contact', 'N/A')) 
        table.add_row(str(client['id']), client['full_name'], client['email'], client['company_name'],sales_contact)

    
    console = Console()
    console.print(table)
else:
    print(f"Failed to retrieve clients. Status code: {response.status_code} - {response.text}")
