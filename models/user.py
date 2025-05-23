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
        try:
            user_data = UserRepository.input_user_data(name, email, age)
            if user_data:
                return cls(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    age=user_data['age']
                )
            return None
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    @classmethod
    def fetch_user_by_name(cls, name):
        try:
            user_data = UserRepository.fetch_users(name)
            if user_data:
                return cls(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    age=user_data['age']
                )
            return None
        except Exception as e:
            print(f"Error fetching user by name: {str(e)}")
            return None
        
    @classmethod
    def find_user_by_email(cls, email):
        try:
            user_data = UserRepository.find_user_by_email(email)
            if user_data:
                return cls(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    age=user_data['age']
                )
            return None
        except Exception as e:
            print(f"Error finding user by email: {str(e)}")
            return None
    
    def update_user(self, param_to_update, new_value):
        """Update a user by their ID"""
        try:
            return UserRepository.update(self.id, param_to_update, new_value)
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None

    def update_user_by_name(self, param_to_update, new_value):
        """Update a user by their name instead of ID"""
        try:
            user = self.fetch_user_by_name(self.name) 
            if user is None:
                return None
            return self.update_user(user.id, param_to_update, new_value)
        except Exception as e:
            print(f"Error updating user by name: {str(e)}")
            return None

    def delete(self):
        try:
            return UserRepository.delete(self.id)
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return None

    @classmethod
    def fetch_all_users(cls):
        try:
            return UserRepository.fetch_all_users()
        except Exception as e:
            print(f"Error fetching all users: {str(e)}")
            return None