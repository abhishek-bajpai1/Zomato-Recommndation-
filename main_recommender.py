import sys
import json
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

def main():
    # Read input from stdin (Next.js will pass preferences as JSON)
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"error": "No input data received"}))
            return
            
        preferences = json.loads(input_data)
        price = preferences.get('price')
        location = preferences.get('location')
        cuisine = preferences.get('cuisine')
        rating = float(preferences.get('rating', 0))

        # 1. Load Data
        if not os.path.exists("zomato_data.csv"):
            print(json.dumps({"error": "Dataset not found. Please run Phase 1."}))
            return
        
        df = pd.read_csv("zomato_data.csv")

        # 2. Filter
        filtered_df = filter_restaurants(df, price=price, place=location, rating=rating, cuisine=cuisine)
        
        if filtered_df.empty:
            print(json.dumps({"recommendations": [], "message": "No restaurants found matching your criteria."}))
            return

        # 3. Rank
        ranked_df = rank_restaurants(filtered_df)

        # 4. Get AI Insight (Top 3)
        engine = RecommendationEngine()
        llm_response = engine.get_recommendations(str(preferences), ranked_df)

        # 5. Format Output
        top_results = ranked_df.head(3).to_dict(orient='records')
        
        # Mapping back to the names the frontend expects
        formatted_results = []
        for res in top_results:
            formatted_results.append({
                "name": res.get('restaurant name'),
                "location": res.get('area'),
                "cuisines": res.get('cuisines type'),
                "rate": f"{res.get('rate (out of 5)')}/5",
                "approx_cost": str(res.get('avg cost (two people)')),
                "description": "Recommended based on your preferences." # Placeholder if LLM fails
            })

        # If LLM response is valid, we could potentially parse it or just include it as a separate field
        # For simplicity, we'll return the formatted results and the raw AI insight
        print(json.dumps({
            "recommendations": formatted_results,
            "ai_insight": llm_response
        }))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
