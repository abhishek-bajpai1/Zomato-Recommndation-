import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class RecommendationEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_recommendations(self, user_preferences, filtered_restaurants):
        """
        Uses Groq LLM to generate natural language recommendations from filtered restaurants (Kaggle schema).
        """
        if filtered_restaurants.empty:
            return "No recommendations returned. Try relaxing filters."

        # Mapping for display in prompt
        col_mapping = {
            'restaurant name': 'name',
            'area': 'location',
            'rate (out of 5)': 'rating',
            'avg cost (two people)': 'cost_for_two',
            'cuisines type': 'cuisines'
        }
        
        # Limit to top 5 and rename columns for LLM clarity
        top_restaurants = filtered_restaurants.head(5).rename(columns=col_mapping)[list(col_mapping.values())].to_dict(orient='records')
        
        prompt = f"""
        User Preferences: {user_preferences}
        
        Available Restaurants:
        {top_restaurants}
        
        Task: Based on the user preferences and the available restaurants, provide 3 clear and concise recommendations. 
        For each restaurant, explain why it matches the user's preferences. 
        Format the response clearly with restaurant names and descriptions.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful Zomato food expert providing restaurant recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"

if __name__ == "__main__":
    import pandas as pd
    # For standalone testing
    engine = RecommendationEngine()
    dummy_data = pd.DataFrame([{
        'restaurant name': 'Test Cafe',
        'area': 'Indore',
        'cuisines type': 'Cafe',
        'rate (out of 5)': 4.5,
        'avg cost (two people)': 500
    }])
    print(engine.get_recommendations("I want a cafe in Indore", dummy_data))
