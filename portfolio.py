from crypto_data import CryptoAsset
from user import User
from database.db import supabase

#handles
class Portfolio:
    def __init__(self, user: User): #passing the User object as a parameter to the class so we can access its attributes like user id and name
        self.user_id = user.id
        self.name = user.name

    def check_quantity(self, asset):
        try:
            response = (
                supabase.table("portfolio")
                .select("quantity")
                .eq("user_id", self.user_id)
                .eq("asset", asset)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0]["quantity"]
            else:
                print(f"No {asset} found for user {self.name}")
                return 0
        except Exception as e:
            print(f"Error checking quantity: {str(e)}")
            return 0
    
    def add_quantity(self, asset, new_value):
        existing = self.check_quantity(asset)
        updated_value = existing + new_value
        return updated_value
    

    def add_asset(self, asset, quantity):
        updated_value = self.add_quantity(asset, quantity)
        try:
            response = (
                supabase.table("portfolio")
                .upsert({"user_id": self.user_id, "asset": asset, "quantity": updated_value},
                on_conflict="user_id,asset") #follow this syntax
                .execute()
            )
            return response.data

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None        
    
    def fetch_user_assets(self):
            response = (
                supabase.table("portfolio")
                .select("*")
                .eq("user_id", self.user_id)
                .execute()
            )
            return response.data
    
    def fetch_singular_asset(self, asset):
            response = (
                supabase.table("portfolio")
                .select("*")
                .eq("asset", asset)
                .execute()
            )
            return response.data    

    def delete_asset(self, asset, quantity):
        quantity = -quantity
        updated_value = self.add_quantity(asset, quantity)
        try:
            response = (
                supabase.table("portfolio")
                .upsert({"user_id": self.user_id, "asset": asset, "quantity": updated_value},
                on_conflict="user_id,asset") #follow this syntax
                .execute()
            )
            return response.data

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None        



user1 = User(8, 'daniel', 'daniel@gmail.com', 16)
user2 = User(12, 'hannah', 'hannah@gmail.com', 20)
portfolio1 = Portfolio(user1)
portfolio2 = Portfolio(user2)
portfolio1.delete_asset('btc', 10)
assets = portfolio1.fetch_user_assets()
print(assets)
print(portfolio1.fetch_singular_asset('btc'))


        

