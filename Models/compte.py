from DB.csv_manager import CSVManager
from Models.transaction import Transaction

transactions_csv_manager = CSVManager('data/transactions.csv')
Transaction.nbr_transactions =  transactions_csv_manager.get_num_rows()

class Compte:
    nbr_comptes = 0

    def __init__(self, owner, account_number=None, balance=0.0):
        if account_number is None:
            Compte.nbr_comptes += 1
            self.account_number = Compte.nbr_comptes
        else:
            self.account_number = account_number
        self.balance = balance
        self.owner = owner
        
        self.list_transactions = self.load_transactions_data()

        Compte.taux_interet = 0.10

    def load_transactions_data(self):
        transactions = transactions_csv_manager.read_data()
        return sorted(
            [
                transaction 
                for transaction in transactions
                if self.account_number in (transaction["source_account"], transaction["destination_account"])
            ],
            key=lambda transaction: transaction["timestamp"]
        )
        
        
    def get_account_number(self):
        return self.account_number
    
    def get_balance(self):
        return self.balance
    
    def get_owner(self):
        return self.owner
    
    def get_transactions_history(self):
        self.list_transactions = self.load_transactions_data()
        return self.list_transactions
    
    def set_balance(self, balance):
        self.balance = balance
        
    def add_transaction(self, transaction):
        self.list_transactions.append(transaction)
    def credit(self, amount):
        self.balance += amount

    def debit(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds. Debit operation failed.")

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'balance': self.balance,
            'owner': self.owner.to_dict()
        }
    
    def save(self):
        csv_manager = CSVManager('data/comptes.csv')
        data = csv_manager.read_data()
        compte_index = next((i for i in range(len(data)) if data[i]["account_number"] == self.account_number), None)
        print(compte_index)
        if compte_index is None:
            new_compte = {
                'account_number': self.account_number,
                'balance': self.balance,
                'ownerID': self.owner.ID
            }
            data.append(new_compte)
        else:
            data[compte_index]['balance'] = self.balance
        
        csv_manager.write_data(data)
