from repositories.user_repository import UserRepository

class User:
    """User class for managing user data and operations.
    
    This class provides methods for creating, retrieving, updating, and deleting users,
    as well as handling user authentication and profile management.
    """
    def __init__(self, id, name, email, age):
        """Initialize a User instance.
        
        Args:
            id (int): Unique identifier for the user
            name (str): User's name
            email (str): User's email address
            age (int): User's age
        """
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def create_user(cls, name, email, age):
        """Create a new user in the database.
        
        Args:
            name (str): User's name
            email (str): User's email address
            age (int): User's age
            
        Returns:
            User: New User instance if creation was successful, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during user creation
        """
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
        """Retrieve a user from the database by their name.
        
        Args:
            name (str): Name of the user to retrieve
            
        Returns:
            User: User instance if found, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during retrieval
        """
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
        """Find a user in the database by their email address.
        
        Args:
            email (str): Email address of the user to find
            
        Returns:
            User: User instance if found, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during search
        """
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
        """Update a specific parameter of the user in the database.
        
        Args:
            param_to_update (str): Name of the parameter to update (e.g., 'name', 'email', 'age')
            new_value: New value for the specified parameter
            
        Returns:
            dict: Updated user data if successful, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during update
        """
        try:
            return UserRepository.update(self.id, param_to_update, new_value)
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None

    # def update_user_by_name(self, param_to_update, new_value):
    #     """Update a user by their name instead of ID"""
    #     try:
    #         return self.update_user(param_to_update, new_value)
    #     except Exception as e:
    #         print(f"Error updating user by name: {str(e)}")
    #         return None

    def delete(self):
        """Delete the user from the database.
        
        Returns:
            bool: True if deletion was successful, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during deletion
        """
        try:
            return UserRepository.delete(self.id)
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return None

    @classmethod
    def fetch_all_users(cls):
        """Retrieve all users from the database.
        
        Returns:
            list: List of dictionaries containing user data if successful, None otherwise
            
        Raises:
            Exception: Prints error message if an exception occurs during retrieval
        """
        try:
            return UserRepository.fetch_all_users()
        except Exception as e:
            print(f"Error fetching all users: {str(e)}")
            return None