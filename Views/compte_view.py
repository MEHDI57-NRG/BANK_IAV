from DB.csv_manager import CSVManager
from Models.user import Compte
from Models.transaction import Transaction
from Controllers.compte_controller import CompteController
from Controllers.transaction_controller import TransactionController

comptes_csv_manager = CSVManager('data/comptes.csv')
Compte.nbr_users =  comptes_csv_manager.get_num_rows()
compte_controller = CompteController(comptes_csv_manager)

transactions_csv_manager = CSVManager('data/transactions.csv')
Transaction.nbr_transactions =  transactions_csv_manager.get_num_rows()
transaction_controller = TransactionController(transactions_csv_manager)

def show_balance(compte):
    print("Your current balance : " + str(compte.get_balance()))
    
def show_compte_transactions_history(compte):
    transactions_history = compte.get_transactions_history()

    print(f"\nHistorique de Transactions de compte {compte.get_account_number()}:")
    for idx, transaction in enumerate(transactions_history):
        print(f"{idx}. Transaction #{transaction['transaction_id']}: timestamp - {transaction['timestamp']} | source_account - {transaction['source_account']} | destination_account - {transaction['destination_account']} | amount - {transaction['amount']}")
    
    print("\n"*2)
          
def show_make_transaction(compte):
    balance = compte.get_balance()
    
    destination_account = compte_controller.get_CompteByNumeroCompte(input("Enter the destination account number: "))
    while destination_account is None:
        print("This account number is not available")
        destination_account = compte_controller.get_CompteByNumeroCompte(input("Enter a valid the destination account number: "))
    
    amount = float(input("Enter the amount: "))
    while(amount > balance):
        print("You havn't enough balance to make transaction")
        amount = float(input("Enter a valid amount: "))
    
    transaction = transaction_controller.make_transaction(compte, destination_account, amount)
    if transaction:
        print("Transaction created successfully")
    else:
        print("Transaction failed")
        
    print("\n"*2)
    
def show_taux_interet():
    print("The intrest rate : ", Compte.taux_interet)     
    print("\n"*2)
    
def show_credit_simulation(compte):
    print("Simulation de crédit")
    
    amount   = float(input("Montant du crédit souhaité : "))
    duration = int(input("Durée du crédit en mois : "))
    
    credit_result = compte_controller.simulate_credit_logic(amount, duration)

    print("\nRésultat de la simulation :")
    print(f"Montant du crédit : {amount}")
    print(f"Durée du crédit : {duration} mois")
    print(f"Intérêt total : {credit_result['total_interest']}")
    print(f"Montant mensuel à rembourser : {credit_result['monthly_payment']}")