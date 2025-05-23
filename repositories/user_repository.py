from database.db import supabase

class UserRepository:
    """Repository class for handling all user related database operations"""

    @staticmethod
    def input_user_data(name, email, age):
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

    @staticmethod
    def fetch_users(name):
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
        
    @staticmethod
    def find_user_by_email(email):
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
        
    @staticmethod
    def update(param_to_update, new_value): 
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

    def delete():
        try:
            response = (
                    supabase.table("users")
                    .delete()
                    .eq("id", self.id)
                    .execute()
                )
            return response
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return None
            
        
    def fetch_all_users():
        try:
            response = (
                supabase.table("users")
                .select("*")
                .execute()
                    )
            return response.model_dump_json()
        except Exception as e:
            print(f"Error updating user: {str(e)}")



