import pandas as pd
import os

def filter_restaurants(df, price=None, place=None, rating=0.0, cuisine=None):
    """
    Filters the Zomato dataset (Kaggle version) based on user preferences.
    """
    filtered_df = df.copy()
    
    # Mapping for Kaggle dataset columns
    col_rate = 'rate (out of 5)'
    col_cost = 'avg cost (two people)'
    col_location = 'area'
    col_cuisines = 'cuisines type'
    col_name = 'restaurant name'

    # Ensure numerical columns are clean (Kaggle dataset is already cleaner)
    # But we'll handle any NAs just in case
    filtered_df[col_rate] = pd.to_numeric(filtered_df[col_rate], errors='coerce').fillna(0.0)
    filtered_df[col_cost] = pd.to_numeric(filtered_df[col_cost], errors='coerce').fillna(0.0)

    # Apply Filters
    if place:
        filtered_df = filtered_df[filtered_df[col_location].str.contains(place, case=False, na=False)]
    
    if cuisine:
        filtered_df = filtered_df[filtered_df[col_cuisines].str.contains(cuisine, case=False, na=False)]
        
    if rating > 0:
        filtered_df = filtered_df[filtered_df[col_rate] >= rating]
        
    if price:
        # Simple price categories (Budget < 500, Mid 500-1500, Premium > 1500)
        if price.lower() == 'budget':
            filtered_df = filtered_df[filtered_df[col_cost] < 500]
        elif price.lower() == 'mid':
            filtered_df = filtered_df[(filtered_df[col_cost] >= 500) & (filtered_df[col_cost] <= 1500)]
        elif price.lower() == 'premium':
            filtered_df = filtered_df[filtered_df[col_cost] > 1500]

    return filtered_df

def get_trending_restaurants(df, top_n=10, min_ratings=500):
    """
    Identifies trending restaurants based on high ratings and a significant number of votes.
    """
    trending_df = df.copy()
    col_rate = 'rate (out of 5)'
    col_votes = 'num of ratings'
    
    # Ensure numeric types
    trending_df[col_rate] = pd.to_numeric(trending_df[col_rate], errors='coerce').fillna(0.0)
    trending_df[col_votes] = pd.to_numeric(trending_df[col_votes], errors='coerce').fillna(0)
    
    # Filter for minimum votes to ensure popularity
    trending_df = trending_df[trending_df[col_votes] >= min_ratings]
    
    # Sort by rating and then by votes
    trending_df = trending_df.sort_values(by=[col_rate, col_votes], ascending=[False, False])
    
    return trending_df.head(top_n)

if __name__ == "__main__":
    if os.path.exists("zomato_data.csv"):
        df = pd.read_csv("zomato_data.csv")
        results = filter_restaurants(df, place="BTM", cuisine="North Indian", rating=4.0)
        print(f"Found {len(results)} restaurants matching criteria.")
        if not results.empty:
            print(results[['restaurant name', 'area', 'rate (out of 5)', 'cuisines type']].head())
    else:
        print("Data file not found. Run Phase 1 first.")
