import requests
from rich.table import Table
from rich.console import Console
import os
from rich.syntax import Syntax
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from datetime import datetime
from datetime import timedelta 



class EventController:
    def __init__(self):        
        self.console = Console()
        
    def event_menu(self):
        """
        This function displays the player menu options.
        This function doesn't take any arguments and doesn't return anything.
        """
        title = Text("Client Menu", style="bold magenta")
        panel = Panel(title, border_style="green")
        self.console.print(panel)
        self.console.print("1. Add new event\n2. Update event\n3. Delete event\n4. Event List\n5. Event assigned to me\n6. Events to assign \n7. Back to menu ", style="bold yellow")
    
    def create_event(self):
        jwt_token = os.getenv('JWT_TOKEN')  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        create_event_url = 'http://127.0.0.1:8000/api/event/'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        event_data = {
            "contract": input("Contract ID : "),  
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "support_contact": input("Support Contact ID : "), 
            "location": input("Location : "),
            "attendees": input(" Number of Attendees : "),
            "notes": input("Notes : "),  
        }
        response = requests.post(create_event_url, headers=headers, json=event_data)
        if response.status_code in [200, 201]:
            self.console.print("Event created successfully.", style="bold green")
            created_event = response.json()
            rprint(created_event)  
        else:
            self.console.print(f"Failed to create event. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
            
            
    def update_event(self):
        jwt_token = os.getenv('JWT_TOKEN')  
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        event_id=input("Event ID : ")
        update_event_url = f'http://127.0.0.1:8000/api/event/{event_id}/'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }   
   
        updated_data = {    
            "contract": input("Contract ID : "),  
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "support_contact": input("Support Contact ID : "), 
            "location": input("Location : "),
            "attendees": input(" Number of Attendees : "),
            "notes": input("Notes : "),  
        }
            
        response = requests.patch(update_event_url, headers=headers, json=updated_data)  


        if response.status_code == 200:
            self.console.print("Event updated successfully.", style="bold green")
            updated_event = response.json()
            rprint(updated_event)  
        else:
            self.console.print(f"Failed to update event. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")

    def delete_event(self):
        jwt_token = os.getenv('JWT_TOKEN')  
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        event_id=input("Event ID : ")
        delete_event_url = 'http://127.0.0.1:8000/api/event/{event_id}/'
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }
        response = requests.delete(delete_event_url, headers=headers)
        if response.status_code in [200, 204]:  
            self.console.print("Event deleted successfully.", style="bold green")
        else:
            self.console.print(f"Failed to delete event. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
    def get_event(self):        
        jwt_token = os.getenv('JWT_TOKEN')  
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        list_events_url = 'http://127.0.0.1:8000/api/event/'   

       
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }

        
        response = requests.get(list_events_url, headers=headers)

        if response.status_code == 200:
            events = response.json()         
            
            table = Table(title="Event List")
            table.add_column("Event ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Contract ID", style="magenta")
            table.add_column("Start Date", style="green")
            table.add_column("End Date", style="yellow")
            table.add_column("Support Contact", style="blue")
            table.add_column("Location", style="red")
            table.add_column("Attendees", style="purple")

            for event in events:
                support_contact = str(event.get('support_contact', 'N/A'))  
                contract_id = str(event.get('contract', 'N/A'))  
                table.add_row(
                    str(event.get('id', 'N/A')),
                    contract_id,
                    str(event.get('start_date', 'N/A')),
                    str(event.get('end_date', 'N/A')),
                    support_contact,
                    str(event.get('location', 'N/A')),
                    str(event.get('attendees', 'N/A'))
                )

            self.console.print(table)
        else:
            self.console.print(f"Failed to retrieve events. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")

    def assigned_event(self):        
        jwt_token = os.getenv('JWT_TOKEN')  
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        list_assigned_events_url = 'http://127.0.0.1:8000/api/support-events'  
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }
        response = requests.get(list_assigned_events_url, headers=headers)
        if response.status_code == 200:
            assigned_events = response.json()     
            
            table = Table(title="Events Assigned to Support User")
            table.add_column("Event ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Contract ID", style="magenta")
            table.add_column("Start Date", style="green")
            table.add_column("End Date", style="yellow")
            table.add_column("Location", style="blue")
            table.add_column("Attendees", style="red")
            table.add_column("Support Contact", style="red")

            
            for event in assigned_events:
                table.add_row(
                    str(event.get('id', 'N/A')),
                    str(event.get('contract', 'N/A')),  
                    str(event.get('start_date', 'N/A')),
                    str(event.get('end_date', 'N/A')),
                    str(event.get('location', 'N/A')),
                    str(event.get('attendees', 'N/A')),
                    str(event.get('support_contact', 'N/A')),
                )

            self.console.print(table)
        else:
            self.console.print(f"Failed to retrieve assigned events. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")

    def nullsupport_event(self):        
        jwt_token = os.getenv('JWT_TOKEN')  
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        list_null_support_events_url = 'http://127.0.0.1:8000/api/null-role-events/'  
        headers = {
            'Authorization': f'Bearer {jwt_token}'
        }
        response = requests.get(list_null_support_events_url, headers=headers)
        if response.status_code == 200:
            events = response.json()            
            table = Table(title="Events Without Assigned Support Contact")
            table.add_column("Event ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Contract ID", style="magenta")
            table.add_column("Start Date", style="green")
            table.add_column("End Date", style="yellow")
            table.add_column("Location", style="blue")
            table.add_column("Attendees", style="red")
            table.add_column("Support", style="red")
            
            for event in events:
                table.add_row(
                    str(event.get('id', 'N/A')),
                    str(event.get('contract', 'N/A')),  
                    str(event.get('start_date', 'N/A')),
                    str(event.get('end_date', 'N/A')),
                    str(event.get('location', 'N/A')),
                    str(event.get('attendees', 'N/A')),
                    str(event.get('support_contact', 'N/A'))
                )

            self.console.print(table)
        else:
            self.console.print(f"Failed to retrieve events. Status code: [bold red]{response.status_code}[/bold red] - {response.text}", style="bold red")
