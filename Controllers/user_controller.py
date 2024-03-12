import hashlib
from Models.user import User
from DB.csv_manager import CSVManager

class UserController:

    def __init__(self, csv_manager):
        self.csv_manager = csv_manager
        self.users_data = self.csv_manager.read_data()

    def register_user(self, user):
        user.save()

    def authenticate_user(self, login, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users_data:
            if user['login'] == login and user['password'] == hashed_password:
                return user['ID']
        return None
            
    def get_personal_info(self, ID):
        user = self.get_UserByID(ID).to_dict()
        if user:
            return user

        return None
        
    def get_account_list(self, ID):
        user = self.get_UserByID(ID)
        if user:
            return user.get_list_comptes()

        return None
    def get_UserByID(self, ID):
        user = next((user for user in self.users_data if user["ID"] == ID), None)
        if user:
            return User(**user)
        else:
            None
    
    def save_data(self):
        self.csv_manager.write_data(self.users_data) 
