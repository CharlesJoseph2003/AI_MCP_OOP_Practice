from database.db import supabase

class UserRepository:
    """Repository class for handling all user related database operations"""

    @staticmethod
    def input_user_data(name, email, age):
        response = (
            supabase.table("portfolio")
            .insert({"name": name, "email": email, "age": age})
            .execute()
        )
        return response

    @staticmethod
    def fetch_users(name):
        response = (
                supabase.table("users")
                .select("*")
                .eq("name", name)
                .execute()
            )
        return response
        
    @staticmethod
    def find_user_by_email(email):
        response = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
            )
        return response
    
    @staticmethod
    def update(param_to_update, new_value):            
        response = (
                supabase.table("users")
                .update({param_to_update: new_value})
                .eq("id", self.id)
                .execute()
            )
        return response

    def delete():
        response = (
                supabase.table("users")
                .delete()
                .eq("id", self.id)
                .execute()
            )
        return response.data
        
    def fetch_all_users():
        response = (
            supabase.table("users")
            .select("*")
            .execute()
                )
        return response



