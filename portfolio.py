from database.db import supabase


class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
    def create_user(self):
        try:
            response = (
                supabase.table("users")
                .insert({"name": self.name, "email": self.email, "age": self.age})
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    def find_user_by_name(self, name):
        """Find a user by their name
        
        Args:
            name: The name of the user to find
            
        Returns:
            The user data or None if not found
        """
        try:
            response = (
                supabase.table("users")
                .select("*")
                .eq("name", name)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0]  # Return the first matching user
            else:
                print(f"No user found with name: {name}")
                return None
        except Exception as e:
            print(f"Error finding user: {str(e)}")
            return None
    
    def update_user(self, user_id, param_to_update, new_value):
        """Update a user by their ID"""
        try:
            response = (
                supabase.table("users")
                .update({param_to_update: new_value})
                .eq("id", user_id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None
            
    def update_user_by_name(self, name, param_to_update, new_value):
        """Update a user by their name instead of ID
        
        Args:
            name: The name of the user to update
            param_to_update: The parameter to update (e.g., 'email', 'age')
            new_value: The new value for the parameter
            
        Returns:
            The updated user data or None if there was an error
        """
        # First find the user by name
        user = self.find_user_by_name(name)
        
        if user is None:
            return None
            
        # Then update the user using their ID
        return self.update_user(user["id"], param_to_update, new_value)


user1 = User('charles', 'charles.joseph2103@gmail.com', 21)
user2 = User('joshua', 'joshua@gmail.com', 13)
# user2.create_user()
print(user1.find_user_by_name('charles'))
user2.update_user_by_name('hanna', 'name', 'hannah')

