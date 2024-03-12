import hashlib

from Models.user import User
from Models.compte import Compte
from Controllers.user_controller import UserController
from Controllers.compte_controller import CompteController
from DB.csv_manager import CSVManager

users_csv_manager = CSVManager('data/users.csv')
User.nbr_users =  users_csv_manager.get_num_rows()
user_controller = UserController(users_csv_manager)

def register_user_interface():
    nom = input("Nom : ")
    prenom = input("Prenom: ")
    login = input("Login: ")
    password = input("Mot de passe: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(
        nom = nom, 
        prenom = prenom, 
        login = login, 
        password = hashed_password)
    
    user_controller.register_user(user)
    print("Inscription réussie!")

def authenticate_user_interface():
    login = input("Login: ")
    password = input("Mot de passe: ")
    user_id = user_controller.authenticate_user(login, password)
    if user_id:
        user = user_controller.get_UserByID(user_id)
        print("Connexion réussie!")
        return user
    else:
        print("Login ou mot de passe incorrect.")
        return None

def show_personal_info(CURRENT_USER):
    user_info = user_controller.get_personal_info(CURRENT_USER.get_ID())
    username = user_info["nom"] + " " + user_info["prenom"]

    print(f"\nInformations personnelles de {username}:")
    print(f"Nom: {user_info['nom']}")
    print(f"Prenom: {user_info['prenom']}")

    print("\n"*2)
    input("Press Any Key to continue...")

def show_account_list(CURRENT_USER):
    account_list = user_controller.get_account_list(CURRENT_USER.get_ID())
    username = CURRENT_USER.get_nom() + " " + CURRENT_USER.get_prenom()

    print(f"\nListe des comptes de {username}:")
    for idx, account in enumerate(account_list):
        print(f"{idx}. Compte #{account['account_number']}: Solde - {account['balance']}")
    
    print("\n"*2)
    input("Press Any Key to continue...")


def show_transactions_history(CURRENT_USER):
    username = CURRENT_USER.get_nom() + " " + CURRENT_USER.get_prenom()
    transactions_history = CURRENT_USER.get_transactions_history()

    print(f"\nHistorique de Transactions de {username}:")
    for idx, transaction in enumerate(transactions_history):
        print(f"{idx}. Transaction #{transaction['transaction_id']}: timestamp - {transaction['timestamp']} | source_account - {transaction['source_account']} | destination_account - {transaction['destination_account']} | amount - {transaction['amount']}")
    
    print("\n"*2)
    input("Press Any Key to continue...")


def show_create_account(owner):
    comptes_csv_manager = CSVManager('data/comptes.csv')
    Compte.nbr_comptes =  comptes_csv_manager.get_num_rows()
    compte_controller = CompteController(comptes_csv_manager)

    username = owner.get_nom() + " " + owner.get_prenom()
    print(f"\nCréation d'un compte de {username}:")
    account_solde = input("Solde du compte : ")
    account = compte_controller.create_compte(owner, account_solde)
    print(f"Compte #{account.get_account_number()}: Solde - {account.get_balance()}")

    print("\n"*2)
    input("Press Any Key to continue...")