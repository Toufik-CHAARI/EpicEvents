


class MainMenu:
    def __init__(self, client_controller,user_controller,contract_controller,event_controller):
        self.client_controller = client_controller
        self.user_controller = user_controller
        self.contract_controller = contract_controller
        self.event_controller = event_controller

    def display_menu(
        self, menu_function, choices_dict, exit_choice=None
    ):
        while True:
            menu_function()
            choice = input("Please select an option: ")
            if exit_choice and choice == exit_choice:
                break
            choices_dict.get(choice, lambda: None)()

    def display(self):
        self.display_menu(
            self.client_controller.main_menu,
            {
                "1": self.client_controller.authenticate,
                "2": self.user_menu_display,
                "3": self.client_menu_display,
                "4": self.contract_menu_display,
                "5": self.event_menu_display,
                "6": self.client_controller.logout,
                "7": exit,
            },
        )
    
    def client_menu_display(self):
        self.display_menu(
            self.client_controller.client_menu,
            {
                "1": self.client_controller.create_client,
                "2": self.client_controller.update_client,
                "3": self.client_controller.delete_client,
                "4": self.client_controller.get_clients,
            },
            "5",
        )
    def user_menu_display(self):
        self.display_menu(
            self.user_controller.user_menu,
            {
                "1": self.user_controller.create_user,
                "2": self.user_controller.update_user,
                "3": self.user_controller.delete_user,
                "4": self.user_controller.get_user,
            },
            "5",
        )
        
    def contract_menu_display(self):
        
        self.display_menu(
            self.contract_controller.contract_menu,
            {
                "1": self.contract_controller.create_contract,
                "2": self.contract_controller.update_contract,
                "3": self.contract_controller.delete_contract,
                "4": self.contract_controller.get_contract,
                "5": self.contract_controller.remaining_amount_contract,
                "6": self.contract_controller.unsigned_contract,
            },
            "7",
        )
        
    def event_menu_display(self):
        
        self.display_menu(
            self.event_controller.event_menu,
            {
                "1": self.event_controller.create_event,
                "2": self.event_controller.update_event,
                "3": self.event_controller.delete_event,
                "4": self.event_controller.get_event,
                "5": self.event_controller.assigned_event,
                "6": self.event_controller.nullsupport_event,
                
            },
            "7",
        )      
        