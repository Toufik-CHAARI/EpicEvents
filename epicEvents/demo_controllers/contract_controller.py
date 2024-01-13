import requests
from rich.table import Table
from rich.console import Console
import os
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text


class ContractController:
    def __init__(self):
        self.console = Console()

    def contract_menu(self):
        """
        Displays the contract management menu with options
        to add, update, delete,list, and view specific types
        of contracts. Presents a styled menu with
        options for the user to choose from.
        """
        title = Text("Client Menu", style="bold magenta")
        panel = Panel(title, border_style="green")
        self.console.print(panel)
        self.console.print(
            "1. Add new contract\n2. Update contract\n"
            "3. Delete contract\n4. Contract List\n"
            "5. Contracts with remaing amount\n"
            "6. Unsigned Contracts \n"
            "7. Back to menu ",
            style="bold yellow",
        )

    def get_contract(self):
        """
        Retrieves and displays a list of contracts from the API.
        Requires authentication with a JWT token. If the token
        is not available, prompts for authentication. Displays
        contracts in a table format.
        """
        jwt_token = os.getenv(
            "JWT_TOKEN"
        )  # Get the token from environment variable
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        list_url = "http://127.0.0.1:8000/api/contract/"
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(list_url, headers=headers)
        if response.status_code == 200:
            contracts = response.json()

            # Create a Rich table
            table = Table(title="Contract List")
            table.add_column(
                "ID", justify="right", style="cyan", no_wrap=True
            )
            table.add_column("Client ID", style="magenta")
            table.add_column("Total Amount", style="green")
            table.add_column("Remaining Amount", style="yellow")
            table.add_column("Creation Date", style="blue")
            table.add_column("Is Signed", style="red")
            table.add_column("sales_contact", style="red")

            for contract in contracts:
                is_signed = (
                    "Yes" if contract.get("is_signed", False) else "No"
                )
                table.add_row(
                    str(contract.get("id", "N/A")),
                    str(contract.get("client", {})),
                    str(contract.get("total_amount", "N/A")),
                    str(contract.get("remaining_amount", "N/A")),
                    str(contract.get("creation_date", "N/A")),
                    is_signed,
                    str(contract.get("sales_contact", "N/A")),
                )

            self.console = Console()
            self.console.print(table)
        else:
            print(
                "Failed to retrieve contracts. Status code:"
                f"{response.status_code} - {response.text}"
            )

    def create_contract(self):
        """
        Prompts the user for contract information and sends a request
        to create a new contract. Requires authentication with a
        JWT token. If the token is not available, prompts for
        authentication. Displays a success message
        and contract details upon successful creation.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        list_url = "http://127.0.0.1:8000/api/contract/"
        headers = {"Authorization": f"Bearer {jwt_token}"}

        contract_data = {
            "client": input("Client ID : "),
            "sales_contact": input("Sales Contact ID : "),
            "total_amount": input("Total Amount : "),
            "remaining_amount": input("Remaining Amount: "),
            "is_signed": input("Is_Signed (True/False): "),
        }

        response = requests.post(
            list_url, headers=headers, json=contract_data
        )

        if response.status_code in [200, 201]:
            self.console.print(
                "Contract created successfully.", style="bold green"
            )
            created_contract = response.json()
            rprint(created_contract)
        else:
            self.console.print(
                "Failed to create contract. Status code: [bold red]"
                f"{response.status_code}[/bold red] - {response.text}",
                style="bold red",
            )

    def update_contract(self):
        """
        Prompts the user for a contract ID and new information
        to update an existing contract. Requires authentication
        with a JWT token. If the token is not available, prompts
        for authentication. Displays a success message and
        updated contract details upon successful update.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        contract_id = input("Contract ID : ")
        update_contract_url = (
            f"http://127.0.0.1:8000/api/contract/{contract_id}/"
        )
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }

        updated_data = {
            "sales_contact": input("Sales Contact ID : "),
            "total_amount": input("Total Amount : "),
            "remaining_amount": input("Remaining Amount: "),
            "is_signed": input("Is_Signed (True/False): "),
        }
        response = requests.patch(
            update_contract_url, headers=headers, json=updated_data
        )
        if response.status_code == 200:
            self.console.print(
                "Contract updated successfully.", style="bold green"
            )
            updated_contract = response.json()
            rprint(updated_contract)
        else:
            self.console.print(
                "Failed to update contract. Status code: [bold red]"
                f"{response.status_code}[/bold red] - {response.text}",
                style="bold red",
            )

    def delete_contract(self):
        """
        Prompts the user for a contract ID to delete the
        corresponding contract.Requires authentication
        with a JWT token. If the token is not available,
        prompts for authentication. Displays a success
        message upon successful deletion of the contract.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        contract_id = input("Contract ID : ")
        d1 = "http://127.0.0.1:8000/api/contract/"
        d2 = f"{contract_id}/"
        delete_contract_url = d1 + d2
        headers = {"Authorization": f"Bearer {jwt_token}"}

        response = requests.delete(delete_contract_url, headers=headers)

        if response.status_code in [200, 204]:
            self.console.print(
                "Contract deleted successfully.", style="bold green"
            )
        else:
            self.console.print(
                "Failed to delete contract."
                "Status code: [bold red]"
                f"{response.status_code}[/bold red] -"
                f"{response.text}",
                style="bold red",
            )

    def remaining_amount_contract(self):
        """
        Retrieves and displays a list of contracts with a remaining
        amount for commercial users. Requires authentication with
        a JWT token. If the token is not available, prompts for
        authentication. Displays contracts in a table format.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        headers = {"Authorization": f"Bearer {jwt_token}"}

        url1 = "http://127.0.0.1:8000/api/contracts/"
        url2 = "commercial/remaining-amount/"
        url = url1 + url2

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            remaining_amount_contracts = response.json()

            table = Table(
                title="Contracts with Remaining Amount for Commercial User"
            )
            table.add_column(
                "Contract ID",
                justify="right",
                style="cyan",
                no_wrap=True,
            )
            table.add_column("Client ID", style="magenta")
            table.add_column("Total Amount", style="green")
            table.add_column("Remaining Amount", style="yellow")
            table.add_column("Creation Date", style="blue")

            for contract in remaining_amount_contracts:
                table.add_row(
                    str(contract.get("id", "N/A")),
                    str(contract.get("client", "N/A")),
                    str(contract.get("total_amount", "N/A")),
                    str(contract.get("remaining_amount", "N/A")),
                    str(contract.get("creation_date", "N/A")),
                )

            self.console.print(table)
        else:
            self.console.print(
                "Failed to retrieve contracts. Status code:"
                f"[bold red]{response.status_code}[/bold red]"
                f" - {response.text}",
                style="bold red",
            )

    def unsigned_contract(self):
        """
        Retrieves and displays a list of unsigned contracts for
        commercial users.Requires authentication with a JWT token.
        If the token is not available,prompts for authentication.
        Displays contracts in a table format.
        """
        jwt_token = os.getenv("JWT_TOKEN")
        if jwt_token is None:
            print("You must be authenticated to view contracts.")
            return
        headers = {"Authorization": f"Bearer {jwt_token}"}
        list_unsigned_contracts_url = (
            "http://127.0.0.1:8000/api/contracts/commercial/unsigned/"
        )
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(
            list_unsigned_contracts_url, headers=headers
        )
        if response.status_code == 200:
            unsigned_contracts = response.json()
            table = Table(
                title="Unsigned Contracts for Commercial User"
            )
            table.add_column(
                "Contract ID",
                justify="right",
                style="cyan",
                no_wrap=True,
            )
            table.add_column("Client ID", style="magenta")
            table.add_column("Total Amount", style="green")
            table.add_column("Remaining Amount", style="yellow")
            table.add_column("Creation Date", style="blue")

            for contract in unsigned_contracts:
                table.add_row(
                    str(contract.get("id", "N/A")),
                    str(contract.get("client", "N/A")),
                    str(contract.get("total_amount", "N/A")),
                    str(contract.get("remaining_amount", "N/A")),
                    str(contract.get("creation_date", "N/A")),
                )

            self.console.print(table)
        else:
            self.console.print(
                "Failed to retrieve unsigned contracts. Status code:"
                f"[bold red]{response.status_code}[/bold red]"
                f" - {response.text}",
                style="bold red",
            )
