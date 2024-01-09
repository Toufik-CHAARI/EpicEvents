from demo_controllers.client_controller import ClientController
from demo_controllers.user_controller import UserController
from demo_controllers.contract_controller import ContractController
from demo_controllers.event_controller import EventController
from viewdemo.main_menu import MainMenu

'''
from controllers.tournament_controller import TournamentController
from views.main_menu import MainMenu
'''

def main():
    client_controller = ClientController()
    user_controller = UserController()
    contract_controller = ContractController()
    event_controller = EventController()    
    main_menu = MainMenu(client_controller,user_controller,contract_controller,event_controller )
    main_menu.display()


if __name__ == "__main__":
    main()