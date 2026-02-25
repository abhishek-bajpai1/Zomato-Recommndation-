class ComplementarityMap:
    """
    Heuristic-based Item Complementarity Graph.
    Defines relationships for meal completion (e.g., Main -> Side -> Dessert).
    """
    
    # Mapping of Primary Item Categories to Recommended Add-On Categories
    CATEGORY_FLOW = {
        "Main Course": ["Sides", "Beverages"],
        "Sides": ["Beverages", "Dessert"],
        "Dessert": ["Beverages"],
    }

    # Specific Item-to-Item mapping (High Confidence)
    ITEM_RULES = {
        "Biryani": ["Raita", "Salan", "Coke", "Gulab Jamun"],
        "Burger": ["Fries", "Wings", "Pepsi", "Large Coke"],
        "Pizza": ["Garlic Bread", "Stuffed Crust", "Choco Lava Cake", "7-Up"],
        "Dosa": ["Filter Coffee", "Vada", "Sambar"],
        "North Indian Thali": ["Lassi", "Buttermilk", "Extra Roti"],
        "Sushi": ["Miso Soup", "Edamame", "Green Tea"],
    }

    @classmethod
    def get_related_items(cls, item_name, existing_cart_items=None):
        """
        Retrieves potential add-ons based on a specific item name.
        """
        related = cls.ITEM_RULES.get(item_name, [])
        
        # Filter out items already in cart
        if existing_cart_items:
            related = [i for i in related if i not in existing_cart_items]
            
        return related

    @classmethod
    def get_contextual_category_needs(cls, cart_categories):
        """
        Identifies missing categories in the meal pattern.
        """
        needs = []
        for cat in cart_categories:
            needs.extend(cls.CATEGORY_FLOW.get(cat, []))
        
        # Return unique missing categories (prioritizing common ones)
        return list(set(needs))
