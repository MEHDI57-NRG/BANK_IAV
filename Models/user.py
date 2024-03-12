from Models.compte import Compte
from Models.transaction import Transaction
from DB.csv_manager import CSVManager

comptes_csv_manager = CSVManager('data/comptes.csv')
Compte.nbr_comptes =  comptes_csv_manager.get_num_rows()

transactions_csv_manager = CSVManager('data/transactions.csv')
Transaction.nbr_transactions =  transactions_csv_manager.get_num_rows()

class User:
    nbr_users = 0
    def __init__(self, **params):
        if params.get('ID'):
            self.ID = params.get('ID')
        else:
            User.nbr_users += 1
            self.ID = User.nbr_users
        self.nom = params.get('nom')
        self.prenom = params.get('prenom')
        self.login = params.get('login')
        self.password = params.get('password')

        self.list_comptes = self.load_comptes_data()
        self.list_transactions = self.load_transactions_data()

    def load_comptes_data(self):
        comptes = comptes_csv_manager.read_data()
        return [compte for compte in comptes if compte["ownerID"] == self.ID]

    def load_transactions_data(self):
        accounts_numbers = {compte["account_number"] for compte in self.list_comptes}
        transactions = transactions_csv_manager.read_data()
        return sorted(
            [transaction for transaction in transactions if
             transaction["source_account"] in accounts_numbers or transaction["destination_account"] in accounts_numbers],
            key=lambda transaction: transaction["timestamp"]
        )


    def get_ID(self):
        return self.ID
    
    def get_nom(self):
        return self.nom
    
    def get_prenom(self):
        return self.prenom
    
    def get_login(self):
        return self.login
    
    def get_password(self):
        return self.password
    
    def set_nom(self, nom):
        self.nom = nom

    def set_prenom(self, prenom):
        self.prenom = prenom
    
    def set_login(self, login):
        self.login = login
    
    def set_password(self, password):
        self.password = password

    def get_list_comptes(self):
        self.list_comptes = self.load_comptes_data()
        return self.list_comptes
    
    def add_compte(self, compte):
        self.list_comptes.append(compte)

    def get_transactions_history(self):
        self.list_transactions = self.load_transactions_data()
        return self.list_transactions
    
    def add_transction(self, transaction):
        self.list_transactions.append(transaction)
        self.transactions = sorted(self.list_transactions, lambda transaction: transaction["timestamp"])

    def to_dict(self):
        return {
            'ID': self.ID,
            'nom': self.nom,
            'prenom': self.prenom,
            'login': self.login,
            'password': self.password
        }
    
    def save(self):
        csv_manager = CSVManager('data/users.csv')
        data = csv_manager.read_data()
        user_index = next((i for i in range(len(data)) if data[i]["ID"] == self.ID), None)
        if user_index:
            data[user_index] = self.to_dict()
        else:
            data.append(self.to_dict())
        csv_manager.write_data(data)