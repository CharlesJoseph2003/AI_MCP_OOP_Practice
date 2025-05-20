from database.db import supabase

class User:
    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    @classmethod
    def create_user(cls, name):
        try:
            response = (
                supabase.table("portfolio")
                .insert({"name": name, "email": email, "age": age})
                .execute()
            )
            return cls(
                id=response.data[0]['id'],
                name=response.data[0]['name'],
                email=response.data[0]['email'],
                age=response.data[0]['age']
            ) #returns a user object of the class

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None


    @classmethod
    def fetch_user_by_name(cls, name):
        try:
            response = (
                supabase.table("users")
                .select("*")
                .eq("name", name)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return cls(
                    id=response.data[0]['id'],
                    name=response.data[0]['name'],
                    email=response.data[0]['email'],
                    age=response.data[0]['age']
            )
            else:
                print(f"No user found with name: {name}")
                return None
        except Exception as e:
            print(f"Error finding user: {str(e)}")
            return None
        
    @classmethod
    def find_user_by_email(cls, email):
        try:
            response = (
                supabase.table("users")
                .select("*")
                .eq("email", email)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                    return cls(
                        id = response.data[0]['id'],
                        name=response.data[0]['name'],
                        email=response.data[0]['email'],
                        age=response.data[0]['age']
            )
            else:
                print(f"No user found with email: {email}")
                return None
        except Exception as e:
            print(f"Error finding user: {str(e)}")
            return None
    

    def update_user(self, param_to_update, new_value):
        """Update a user by their ID"""
        try:
            response = (
                supabase.table("users")
                .update({param_to_update: new_value})
                .eq("id", self.id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None


    def update_user_by_name(self, param_to_update, new_value):
        """Update a user by their name instead of ID"""
        # First find the user by name
        user = self.fetch_user_by_name(self.name)
        
        if user is None:
            return None
            
        # Then update the user using their ID
        return self.update_user(user.id, param_to_update, new_value)
    

  
    def delete(self):
        try:
            response = (
                supabase.table("users")
                .delete()
                .eq("id", self.id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return None


    @classmethod
    def fetch_all_users(cls):
        try:
            response = (
                supabase.table("users")
                .select("*")
                .execute()
                )
            return response.model_dump_json()
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None
