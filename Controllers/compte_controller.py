from Models.user import User
from Controllers.user_controller import UserController
from Models.compte import Compte
from DB.csv_manager import CSVManager

users_csv_manager = CSVManager('data/users.csv')
User.nbr_users =  users_csv_manager.get_num_rows()
user_controller = UserController(users_csv_manager)

class CompteController:

    def __init__(self, csv_manager):
        self.csv_manager = csv_manager
        self.compte_data = self.csv_manager.read_data()

    def create_compte(self, owner, balance):
        compte = Compte(owner, balance)
        compte.save()
        return compte
    
    def get_CompteByNumeroCompte(self, numero_compte):
        compte = next((compte for compte in self.compte_data if compte["account_number"] == numero_compte), None)
        owner = user_controller.get_UserByID(compte["ownerID"])
        if compte:
            return Compte(
                account_number=compte["account_number"],
                owner=owner,
                balance=float(compte["balance"]),
            )
        return compte
    
    def simulate_credit_logic(self, amount, duration):
        annual_interest_rate = Compte.taux_interet
        
        monthly_interest_rate = annual_interest_rate / 12
        
        total_interest = amount * monthly_interest_rate * duration

        monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -duration)

        return {'total_interest': total_interest, 'monthly_payment': monthly_payment}
