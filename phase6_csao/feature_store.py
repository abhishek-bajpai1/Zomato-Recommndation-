import random

class FeatureStore:
    """
    Mock Feature Store for CSAO Ranking.
    Simulates retrieving User, Restaurant, and Item features for real-time inference.
    """

    def __init__(self):
        # Mock Item Features
        self.item_features = {
            "Coke": {"category": "Beverages", "price": 45, "is_veg": True, "popularity": 0.95},
            "Pepsi": {"category": "Beverages", "price": 40, "is_veg": True, "popularity": 0.92},
            "Fries": {"category": "Sides", "price": 95, "is_veg": True, "popularity": 0.88},
            "Raita": {"category": "Sides", "price": 30, "is_veg": True, "popularity": 0.85},
            "Salan": {"category": "Sides", "price": 0, "is_veg": True, "popularity": 0.82},
            "Gulab Jamun": {"category": "Dessert", "price": 60, "is_veg": True, "popularity": 0.89},
            "Garlic Bread": {"category": "Sides", "price": 120, "is_veg": True, "popularity": 0.91},
            "Choco Lava Cake": {"category": "Dessert", "price": 110, "is_veg": True, "popularity": 0.93},
        }

    def get_item_data(self, item_name):
        return self.item_features.get(item_name, {
            "category": "General", 
            "price": 50, 
            "is_veg": True, 
            "popularity": 0.5
        })

    def get_user_context(self, user_id):
        """
        Returns high-level user preferences.
        """
        return {
            "is_premium": random.random() > 0.8,
            "pref_veg": random.random() > 0.3,
            "avg_order_value": 450,
            "dessert_affinity": 0.75
        }

    def get_temporal_context(self):
        """
        Detects current meal session based on hour.
        """
        from datetime import datetime
        hour = datetime.now().hour
        
        if 5 <= hour < 11: return "Breakfast"
        if 11 <= hour < 16: return "Lunch"
        if 16 <= hour < 19: return "Snack"
        if 19 <= hour < 23: return "Dinner"
        return "Late Night"
