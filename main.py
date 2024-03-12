import os
import shutil

from Controllers.user_controller import UserController
from Controllers.compte_controller import CompteController
from DB.csv_manager import CSVManager
from Models.user import User
from Models.compte import Compte
from Views.user_view import register_user_interface, authenticate_user_interface, show_personal_info, show_account_list, show_transactions_history, show_create_account
from Views.compte_view import show_balance, show_compte_transactions_history, show_make_transaction, show_taux_interet, show_credit_simulation
def clear_screen():
    os_name = os.name
    if os_name == 'posix':
        os.system('clear')
    elif os_name == 'nt':
        os.system('cls')
    else:
        print("Clear screen not supported for this operating system.")

def menu():
    terminal_width = shutil.get_terminal_size().columns
    header = "Bienvenue à Bank IAV"
    spaces_before = (terminal_width - len(header)) // 2

    print("\n" + "=" * terminal_width)
    print(" " * spaces_before + header)
    print("=" * terminal_width)

    print("1. Nouvelle Inscription")
    print("2. Connexion au Compte")
    print("3. Quitter")
    print("=" * terminal_width)
    
    choice = input("Veuillez choisir une option: ").strip()
    return choice

def user_menu():
    global CURRENT_USER
    username = CURRENT_USER.get_nom() + " " + CURRENT_USER.get_prenom()

    while True:
        clear_screen()
        terminal_width = shutil.get_terminal_size().columns
        header = f"Bienvenue à Bank IAV, {username}!"
        spaces_before = (terminal_width - len(header)) // 2

        print("\n" + "=" * terminal_width)
        print(" " * spaces_before + header)
        print("=" * terminal_width)

        print("1. Voir mes informations personnelles")
        print("2. Voir la liste de mes comptes")
        print("3. Accéder au compte")
        print("4. Voir historique chronologique de mes transactions")
        print("5. Créer un compte")
        print("6. Se déconnecter")
        print("=" * terminal_width)
        
        choice = input("Veuillez choisir une option: ").strip()

        if choice == '1':
            show_personal_info(CURRENT_USER)

        elif choice == '2':
            show_account_list(CURRENT_USER)
        
        elif choice == '3':
            indice = int(input("Choisi un compte: ").strip())
            numero_compte = CURRENT_USER.get_list_comptes()[indice-1]['account_number']
            compte_menu(numero_compte)

        elif choice == '4':
            show_transactions_history(CURRENT_USER)
        
        elif choice == '5':
            show_create_account(CURRENT_USER)

        elif choice == '6':
            print("\n"*2+"Vous etes bien déconnectée"+"\n"*2)
            break

        else:
            print("Option invalide. Veuillez réessayer.")

def compte_menu(numero_compte):
    global CURRENT_USER
    comptes_csv_manager = CSVManager('data/comptes.csv')
    Compte.nbr_comptes =  comptes_csv_manager.get_num_rows()
    compte_controller = CompteController(comptes_csv_manager)


    compte = compte_controller.get_CompteByNumeroCompte(numero_compte)
    CURRENT_USER = compte.get_owner()
    username = CURRENT_USER.get_nom() + " " + CURRENT_USER.get_prenom()

    while True:
        clear_screen()
        terminal_width = shutil.get_terminal_size().columns
        header = f"Compte {numero_compte}"
        spaces_before = (terminal_width - len(header)) // 2
        print("\n" + "=" * terminal_width)
        print(" " * spaces_before + header)
        print("=" * terminal_width)

        print("1. Consultation de solde")
        print("2. Voir historique de transactions")
        print("3. Effectuer un transfert d'argent")
        print("4. Consulter le taux d'intérêt actuel")
        print("5. Simulation d'un crédit")
        print("6. Quitter")
            
        choice = input("Veuillez choisir une option: ").strip()

        if choice == '1':
            show_balance(compte)

        elif choice == '2':
            show_compte_transactions_history(compte)
            
        elif choice == '3':
            show_make_transaction(compte)
        elif choice == '4':
            show_taux_interet()
        elif choice == '5':
            show_credit_simulation(compte)

        elif choice == '6':
            break

        else:
            print("Option invalide. Veuillez réessayer.")
        
        input("Press Any Key to continue...    ")

def handle_choice(choice):
    global CURRENT_USER
    menu_functions = {
        '1': register_user_interface,
        '2': authenticate_user_interface,
        '3': exit_program,
    }
    selected_function = menu_functions.get(choice, invalid_option)
    if choice == '2':
        CURRENT_USER = selected_function()
        if CURRENT_USER:
            user_menu()
    else:
        selected_function()

def exit_program():
    print("Programme terminé.")
    exit()

def invalid_option(user_controller):
    print("Option invalide. Veuillez réessayer.")

def main():

    while True:
        clear_screen()
        choice = menu()
        handle_choice(choice)
        print("\n"*2)
        input("Press Any Key to continue...    ")

if __name__ == "__main__":
    main()
