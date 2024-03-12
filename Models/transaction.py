from datetime import datetime
from DB.csv_manager import CSVManager

class Transaction:
    nbr_transactions = 0

    def __init__(self, source_account, destination_account, amount, transaction_id=None, timestamp = None):
        if transaction_id is None:
            Transaction.nbr_transactions += 1
            self.transaction_id = Transaction.nbr_transactions
        else:
            transaction_id = transaction_id
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = datetime.strptime(timestamp, 'YYYY-MM-DD HH:MM:SS.mmmmmm')
        self.source_account = source_account
        self.destination_account = destination_account
        self.amount = amount

    def get_transaction_id(self):
        return self.transaction_id
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_source_account(self):
        return self.source_account
    
    def get_destination_account(self):
        return self.destination_account
    
    def get_amount(self):
        return self.amount
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'timestamp': self.timestamp.isoformat(),
            'source_account': self.source_account.get_account_number(),
            'destination_account': self.destination_account.get_account_number(),
            'amount': self.amount
        }
    
    def save(self):
        csv_manager = CSVManager('data/transactions.csv')
        data = csv_manager.read_data()
        transaction_index = next((i for i in range(len(data)) if data[i]["transaction_id"] == self.transaction_id), None)
        if transaction_index:
            data[transaction_index] = self.to_dict()
        else:
            data.append(self.to_dict())
        csv_manager.write_data(data)

