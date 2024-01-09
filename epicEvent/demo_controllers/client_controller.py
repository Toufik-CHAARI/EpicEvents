import requests
from rich.table import Table
from rich.console import Console
import os
from getpass import getpass 
from rich.syntax import Syntax
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

class ClientController:
    def __init__(self):
        self.console = Console()
        
    def authenticate(self):
        self.console.print("Please enter your credentials:")
        username = input("Username: ")
        password = getpass("Password: ")

        token_url = 'http://127.0.0.1:8000/api-auth/api/token/'
        credentials = {
            'username': username,
            'password': password
        }

        response = requests.post(token_url, data=credentials)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access']
            os.environ['JWT_TOKEN'] = access_token
            self.console.print("Authentication successful. Access token retrieved.", style="bold green")
        else:
            self.console.print(f"Failed to authenticate. Status code: {response.status_code} - {response.text}", style="bold red")

    def logout(self):
        if 'JWT_TOKEN' in os.environ:
            del os.environ['JWT_TOKEN']
            self.console.print("Logged out successfully.", style="bold green")
        else:
            self.console.print("You are not logged in.", style="bold red")
    
    def main_menu(self):
        """
        This function displays the main menu options.
        This function doesn't take any arguments and doesn't return anything.
        """
        title = Text("Main Menu", style="bold magenta")
        panel = Panel(title, border_style="blue")
        self.console.print(panel)
        self.console.print("1. Authentication\n2. Users\n3. Clients\n4. Contracts\n5. Events\n6. Logout\n7. Quit", style="bold yellow")

        
    def client_menu(self):
        """
        This function displays the player menu options.
        This function doesn't take any arguments and doesn't return anything.
        """
        title = Text("Client Menu", style="bold magenta")
        panel = Panel(title, border_style="green")
        self.console.print(panel)
        self.console.print("1. Add new client\n2. Update client\n3. Delete client\n4. Client List\n5. Back to menu", style="bold yellow")
        

    
    def get_clients(self):
        jwt_token = os.getenv('JWT_TOKEN')  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        list_url = 'http://127.0.0.1:8000/api/client'
        headers = {
            'Authorization': f'Bearer {jwt_token}'
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
        
    def create_client(self):
        jwt_token = os.getenv('JWT_TOKEN')  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        create_url = 'http://127.0.0.1:8000/api/client/'       

        # Headers with JWT token
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }

        # Client data to be created
        client_data = {
            "full_name": input("Full Name: "),
            "email": input("Email: "),
            "phone" : input("Phone: "),
            "company_name" : input("company_name: "),
            "creation_date" :input("creation_date: "),
            "last_update" :input("last_update: "),
            
        }
       
        response = requests.post(create_url, headers=headers, json=client_data)
        if response.status_code in [200, 201]:
            client_created = response.json()
            self.console.print("Client created successfully.", style="bold green")
            json_syntax = Syntax(str(client_created), "json", theme="monokai", line_numbers=True)
            self.console.print(json_syntax)
        else:
            error_message = f"Failed to create client. Status code: {response.status_code} - {response.text}"
            self.console.print(error_message, style="bold red")
            
    def update_client(self):
        jwt_token = os.getenv('JWT_TOKEN')  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        client_id= input("Client ID : ")
        update_url = f'http://127.0.0.1:8000/api/client/{client_id}/'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        updated_data = {
            "full_name": input("Full Name: "),
            "email": input("Email: "),
            "phone" : input("Phone: "),
            "company_name" : input("company_name: "),            
            "last_update" :input("last_update: "),
         
        }
        response = requests.patch(update_url, headers=headers, json=updated_data)
        if response.status_code == 200:
            print("Client updated successfully.")
        else:
            print(f"Failed to update client. Status code: {response.status_code} - {response.text}")
        if response.status_code in [200, 201]:
            client_updated = response.json()
            self.console.print("Client updated successfully.", style="bold green")
            json_syntax = Syntax(str(client_updated), "json", theme="monokai", line_numbers=True)
            self.console.print(json_syntax)
        else:
            error_message = f"Failed to update client. Status code: {response.status_code} - {response.text}"
            self.console.print(error_message, style="bold red")
    
    def delete_client(self):
        jwt_token = os.getenv('JWT_TOKEN')  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        client_id= input("Client ID : ")
        delete_event_url = f'http://127.0.0.1:8000/api/client/{client_id}/'  
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }
        response = requests.delete(delete_event_url, headers=headers)
        if response.status_code in [200, 204]:  
            self.console.print("Client deleted successfully.", style="bold green")
        else:
            self.console.print(f"Failed to delete Client. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
