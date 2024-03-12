from Models.transaction import Transaction
from Models.compte import Compte
from Controllers.compte_controller import CompteController

from DB.csv_manager import CSVManager

comptes_csv_manager = CSVManager('data/comptes.csv')
Compte.nbr_comptes =  comptes_csv_manager.get_num_rows()
compte_controller = CompteController(comptes_csv_manager)

class TransactionController:

    def __init__(self, csv_manager):
        self.csv_manager = csv_manager
        self.transaction_data = self.csv_manager.read_data()
    
    def get_TransactionById(self, transaction_id):
        transaction = next((transaction for transaction in self.transaction_data if transaction["transaction_id"] == transaction_id), None)
        if comptes_csv_manager:
            return Transaction(
                transaction_id = transaction["transaction_id"],
                timestamp = transaction["timestamp"],
                source_account = compte_controller.get_CompteByNumeroCompte(transaction["source_account"]),
                destination_account = compte_controller.get_CompteByNumeroCompte(transaction["destination_account"]),
                amount = float(transaction["amount"]),
            )
        return comptes_csv_manager
    
    def make_transaction(self, source_account, destination_acount, amount):
        transaction = Transaction(source_account, destination_acount, amount)
        transaction.save()
        source_account.debit(amount)
        source_account.save()
        return transaction