# from database.db import supabase
from repositories.user_repository import UserRepository

class User:
    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def create_user(cls, name, email, age):
        return UserRepository.input_user_data(name, email, age)

    @classmethod
    def fetch_user_by_name(cls, name):
        return UserRepository.fetch_users(name)
        
    @classmethod
    def find_user_by_email(cls, email):
        return UserRepository.find_user_by_email(email)
    
    def update_user(self, param_to_update, new_value):
        """Update a user by their ID"""
        return UserRepository.update(param_to_update, new_value)

    def update_user_by_name(self, param_to_update, new_value):
        """Update a user by their name instead of ID"""
        user = self.fetch_user_by_name(self.name) 
        if user is None:
            return None
        return self.update_user(user.id, param_to_update, new_value)

    def delete(self):
        return UserRepository.delete()

    @classmethod
    def fetch_all_users(cls):
        return UserRepository.fetch_all_users()