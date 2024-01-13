import requests
from rich.table import Table
from rich.console import Console
import os
from getpass import getpass
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text


class ClientController:
    def __init__(self):
        self.console = Console()

    def authenticate(self):
        """
        Authenticates the user by taking username and password
        inputs.Upon successful authentication, it stores the
        JWT token in an environment variable.
        In case of failure, displays an error message.
        """
        self.console.print("Please enter your credentials:")
        username = input("Username: ")
        password = getpass("Password: ")

        token_url = "http://127.0.0.1:8000/api-auth/api/token/"
        credentials = {"username": username, "password": password}

        response = requests.post(token_url, data=credentials)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access"]
            os.environ["JWT_TOKEN"] = access_token
            self.console.print(
                "Authentication successful. Access token retrieved.",
                style="bold green",
            )
        else:
            self.console.print(
                f"Failed to authenticate. Status code: "
                f"{response.status_code} - {response.text}",
                style="bold red",
            )

    def logout(self):
        """
        Logs out the current user.
        Removes the JWT token from the environment variables.
        Displays a message indicating successful logout or that
        the user was not logged in.
        """
        if "JWT_TOKEN" in os.environ:
            del os.environ["JWT_TOKEN"]
            self.console.print(
                "Logged out successfully.", style="bold green"
            )
        else:
            self.console.print(
                "You are not logged in.", style="bold red"
            )

    def main_menu(self):
        """
        Displays the main menu options using Rich library features.
        Presents a styled list of functionalities including
        authentication, user management, client management,
        contract management, event management,
        logout, and quit options.
        """
        title = Text("Main Menu", style="bold magenta")
        panel = Panel(title, border_style="blue")
        self.console.print(panel)
        self.console.print(
            "1. Authentication\n2. Users\n3. Clients\n4. Contracts\n"
            "5. Events\n6. Logout\n7. Quit",
            style="bold yellow",
        )

    def client_menu(self):
        """
        Displays the client management menu options using Rich
        library features.Offers a styled list of options for adding,
        updating, deleting clients,
        viewing the client list, and returning to the main menu.
        """
        title = Text("Client Menu", style="bold magenta")
        panel = Panel(title, border_style="green")
        self.console.print(panel)
        self.console.print(
            "1. Add new client\n2. Update client\n3. Delete client\n"
            "4. Client List\n5. Back to menu",
            style="bold yellow",
        )

    def get_clients(self):
        """
        Retrieves a list of clients from the API and displays
        them in a table.Requires authentication with a JWT token.
        If the token is not available, it prompts for authentication.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        list_url = "http://127.0.0.1:8000/api/client"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(list_url, headers=headers)
        if response.status_code == 200:
            clients = response.json()
            table = Table(title="Client List")
            table.add_column(
                "ID", justify="right", style="cyan", no_wrap=True
            )
            table.add_column("Full Name", style="magenta")
            table.add_column("Email", style="green")
            table.add_column("Company Name", style="yellow")
            table.add_column("Sales Contact", style="blue")
            table.add_column("Creation Date", style="green")
            table.add_column("Creation Date", style="yellow")
            table.add_column("Phone", style="blue")
            for client in clients:
                sales_contact = str(client.get("sales_contact", "N/A"))
                table.add_row(
                    str(client["id"]),
                    client["full_name"],
                    client["email"],
                    client["company_name"],
                    sales_contact,
                    client["creation_date"],
                    client["last_update"],
                    client["phone"],
                )
            console = Console()
            console.print(table)
        else:
            print(
                f"Failed to retrieve clients. Status code:"
                f"{response.status_code} - {response.text}"
            )

    def create_client(self):
        """
        Prompts the user for client information and sends a request
        to create a new client.Requires authentication with a JWT
        token. If the token is not available, it prompts for
        authentication.Displays a success message and client
        details upon successful creation.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        create_url = "http://127.0.0.1:8000/api/client/"

        headers = {"Authorization": f"Bearer {jwt_token}"}

        client_data = {
            "full_name": input("Full Name: "),
            "email": input("Email: "),
            "phone": input("Phone: "),
            "company_name": input("company_name: "),
        }

        response = requests.post(
            create_url, headers=headers, json=client_data
        )
        if response.status_code in [200, 201]:
            client_created = response.json()
            self.console.print(
                "Client created successfully.", style="bold green"
            )
            json_syntax = Syntax(
                str(client_created),
                "json",
                theme="monokai",
                line_numbers=True,
            )
            self.console.print(json_syntax)
        else:
            error_msg_1 = "Failed to create client."
            error_msg_2 = f"Status code: {response.status_code}"
            error_msg_3 = f" - {response.text}"
            error_message = error_msg_1 + error_msg_2 + error_msg_3
            self.console.print(error_message, style="bold red")

    def update_client(self):
        """
        Prompts the user for a client ID and new client information
        to update an existing client.Requires authentication with a
        JWT token. If the token is not available, it prompts for
        authentication.Displays a success message and updated
        client details upon successful update.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        client_id = input("Client ID : ")
        update_url = f"http://127.0.0.1:8000/api/client/{client_id}/"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
        updated_data = {
            "full_name": input("Full Name: "),
            "email": input("Email: "),
            "phone": input("Phone: "),
            "company_name": input("company_name: "),
        }
        response = requests.patch(
            update_url, headers=headers, json=updated_data
        )
        if response.status_code == 200:
            print("Client updated successfully.")
        else:
            print(
                f"Failed to update client. Status code:"
                f"{response.status_code} - {response.text}"
            )
        if response.status_code in [200, 201]:
            client_updated = response.json()
            self.console.print(
                "Client updated successfully.", style="bold green"
            )
            json_syntax = Syntax(
                str(client_updated),
                "json",
                theme="monokai",
                line_numbers=True,
            )
            self.console.print(json_syntax)
        else:
            error_mes1 = "Failed to update client."
            error_mes2 = f"Status code: {response.status_code} "
            error_mes3 = f"- {response.text}"
            error_message = error_mes1 + error_mes2 + error_mes3
            self.console.print(error_message, style="bold red")

    def delete_client(self):
        """
        Prompts the user for a client ID to delete the corresponding
        client.Requires authentication with a JWT token. If the token
        is not available, it prompts for authentication.Displays a
        success message upon successful deletion of the client.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view clients.")
            return
        client_id = input("Client ID : ")
        delete_event_url = (
            f"http://127.0.0.1:8000/api/client/{client_id}/"
        )
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.delete(delete_event_url, headers=headers)
        if response.status_code in [200, 204]:
            self.console.print(
                "Client deleted successfully.", style="bold green"
            )
        else:
            self.console.print(
                "Failed to delete Client. Status code: [bold red]"
                f"{response.status_code}[/bold red] - {response.text}",
                style="bold red",
            )
