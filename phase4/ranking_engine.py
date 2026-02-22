import pandas as pd
import os

def rank_restaurants(filtered_df):
    """
    Ranks filtered restaurants based on a combination of rating and popularity (votes).
    """
    if filtered_df.empty:
        return filtered_df

    # Scoring formula: 70% rating + 30% normalized votes
    # Normalize 'num of ratings' (votes) to 0-5 scale
    max_votes = filtered_df['num of ratings'].max()
    if max_votes > 0:
        filtered_df['normalized_votes'] = (filtered_df['num of ratings'] / max_votes) * 5
    else:
        filtered_df['normalized_votes'] = 0

    filtered_df['score'] = (filtered_df['rate (out of 5)'] * 0.7) + (filtered_df['normalized_votes'] * 0.3)
    
    # Sort by score descending
    ranked_df = filtered_df.sort_values(by='score', ascending=False)
    
    return ranked_df

if __name__ == "__main__":
    from phase2.recommender_core import filter_restaurants
    
    if os.path.exists("zomato_data.csv"):
        df = pd.read_csv("zomato_data.csv")
        filtered = filter_restaurants(df, place="Bellandur", rating=3.5)
        ranked = rank_restaurants(filtered)
        print("Top 5 Ranked Restaurants in Bellandur:")
        print(ranked[['restaurant name', 'rate (out of 5)', 'num of ratings', 'score']].head())
    else:
        print("Data file not found. Run Phase 1 first.")
