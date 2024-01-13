import requests
from rich.table import Table
from rich.console import Console
import os
from rich.syntax import Syntax

from rich.panel import Panel
from rich.text import Text


class UserController:
    def __init__(self):
        self.console = Console()

    def user_menu(self):
        """
        This function displays the player menu options.
        This function doesn't take any arguments and doesn't return anything.
        """
        title = Text("Client Menu", style="bold magenta")
        panel = Panel(title, border_style="green")
        self.console.print(panel)
        self.console.print(
            "1. Add new user\n2. Update user\n"
            "3. Delete user\n4. User List\n5. Back to menu",
            style="bold yellow",
        )

    def get_user(self):
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view users.")
            return
        list_url = "http://127.0.0.1:8000/api-auth/users"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(list_url, headers=headers)
        if response.status_code == 200:
            users = response.json()

            table = Table(title="User List")

            table.add_column(
                "ID", justify="right", style="cyan", no_wrap=True
            )
            table.add_column("Username", style="magenta")
            table.add_column("Email", style="green")
            table.add_column("Role", style="green")

            for user in users:
                table.add_row(
                    str(user["id"]),
                    user["username"],
                    user["email"],
                    user["role"],
                )

            console = Console()
            console.print(table)
        else:
            print(
                "Failed to retrieve users. Status code:"
                f"{response.status_code} - {response.text}"
            )

    def create_user(self):
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view users.")
            return
        create_user_url = "http://127.0.0.1:8000/api-auth/users/create/"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        user_data = {
            "username": input("Username : "),
            "email": input("Email : "),
            "role": input("Role : "),
            "password": input("Password : "),
        }
        response = requests.post(
            create_user_url, headers=headers, json=user_data
        )
        if response.status_code in [200, 201]:
            user_created = response.json()
            self.console.print(
                "User created successfully.", style="bold green"
            )

            # Using Rich for JSON formatting
            json_syntax = Syntax(
                str(user_created),
                "json",
                theme="monokai",
                line_numbers=True,
            )
            self.console.print(json_syntax)
        else:
            error_m1 = "Failed to create user. Status code:"
            error_m2 = f" {response.status_code} - {response.text}"
            error_message = error_m1 + error_m2
            self.console.print(error_message, style="bold red")

    def update_user(self):
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to update users.")
            return
        user_id = input("User ID : ")
        update_url = (
            f"http://127.0.0.1:8000/api-auth/users/{user_id}/update/"
        )
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
        user_data = {
            "username": input("Username : "),
            "email": input("Email"),
            "role": input("Role : "),
        }
        response = requests.patch(
            update_url, headers=headers, json=user_data
        )
        if response.status_code == 200:
            print("User updated successfully.")
        else:
            print(
                "Failed to update user. Status code: "
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
            error_m1 = "Failed to update client. Status code:"
            error_m2 = f" {response.status_code} - {response.text}"
            error_message = error_m1 + error_m2
            self.console.print(error_message, style="bold red")

    def delete_user(self):
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to update users.")
            return
        user_id = input("User ID : ")
        delete_user_url = (
            f"http://127.0.0.1:8000/api-auth/users/{user_id}/delete/"
        )
        headers = {"Authorization": f"Bearer {jwt_token}"}

        response = requests.delete(delete_user_url, headers=headers)
        if response.status_code in [200, 204]:
            self.console.print(
                "User deleted successfully.", style="bold green"
            )
        else:
            error_m1 = "Failed to delete user. Status code:"
            error_m2 = f" {response.status_code} - {response.text}"
            error_message = error_m1 + error_m2
            self.console.print(error_message, style="bold red")
