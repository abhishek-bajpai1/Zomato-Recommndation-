import unittest
import pandas as pd
import os
from recommender_core import filter_restaurants

class TestPhase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists("zomato_data.csv"):
            cls.df = pd.read_csv("zomato_data.csv")
        else:
            raise FileNotFoundError("Run Phase 1 test first to generate data.")

    def test_filtering_by_place(self):
        # Using 'Bellandur' which is present in the Kaggle dataset
        results = filter_restaurants(self.df, place="Bellandur")
        self.assertLess(len(results), len(self.df))
        self.assertGreater(len(results), 0)
        print(f"Filtered by Bellandur: {len(results)} matches")

    def test_filtering_by_rating(self):
        results = filter_restaurants(self.df, rating=4.5)
        self.assertTrue((results['rate (out of 5)'] >= 4.5).all())
        print(f"Filtered by rating 4.5+: {len(results)} matches")

if __name__ == "__main__":
    unittest.main()
