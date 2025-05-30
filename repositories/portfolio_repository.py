from database.db import supabase

class PortfolioRepository:
    """Repository class for handling all portfolio-related database operations"""
    
    @staticmethod
    def check_asset_quantity(user_id, asset):
        """Check the quantity of a specific asset for a user"""
        try:
            response = (
                supabase.table("portfolio")
                .select("quantity")
                .eq("user_id", user_id)
                .eq("asset", asset)
                .execute()
            )
            
            if response.data and len(response.data) > 0:
                return response.data[0]["quantity"]
            else:
                return 0
        except Exception as e:
            print(f"Error checking quantity: {str(e)}")
            return 0
    
    @staticmethod
    def add_or_update_asset(user_id, asset, quantity):
        """Add or update an asset in a user's portfolio"""
        try:
            response = (
                supabase.table("portfolio")
                .upsert(
                    {"user_id": user_id, "asset": asset, "quantity": quantity},
                    on_conflict="user_id,asset"
                )
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error adding/updating asset: {str(e)}")
            return None
    
    @staticmethod
    def fetch_user_assets(user_id):
        """Fetch all assets for a specific user"""
        try:
            response = (
                supabase.table("portfolio")
                .select("asset, quantity")
                .eq("user_id", user_id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error fetching user assets: {str(e)}")
            return []
    
    @staticmethod
    def fetch_asset(user_id, asset):
        """Fetch a specific asset for a specific user"""
        try:
            response = (
                supabase.table("portfolio")
                .select("asset, quantity")
                .eq("user_id", user_id)
                .eq("asset", asset)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error fetching user asset: {str(e)}")
            return []
