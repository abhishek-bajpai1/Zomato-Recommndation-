import pandas as pd
import os
import sys

# Add project root to path to import local modules
sys.path.append(os.getcwd())

from phase2.recommender_core import filter_restaurants

def run_verification():
    print("--- Phase 2: Robust Filter Verification ---")
    if not os.path.exists("zomato_data.csv"):
        print("FAIL: zomato_data.csv missing!")
        return

    df = pd.read_csv("zomato_data.csv")
    
    test_cases = [
        {"place": "Bellandur", "cuisine": "North Indian", "rating": 4.0, "price": "mid"},
        {"place": "Indiranagar", "cuisine": "Italian", "rating": 4.5, "price": "premium"},
        {"place": "Koramangala", "cuisine": "Cafe", "rating": 3.5, "price": "budget"},
        {"place": "NonExistentPlace", "cuisine": "MarsFood", "rating": 5.0, "price": "cheap"}, # Edge case
    ]

    for i, case in enumerate(test_cases):
        results = filter_restaurants(df, **case)
        print(f"Test case {i+1} ({case['place']}, {case['cuisine']}): {len(results)} matches found.")
        if i == 3: # Check edge case
            if len(results) == 0:
                print("  EDGE CASE: Correctly handled non-existent location.")
            else:
                print("  WARNING: Results found for non-existent location!")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()
