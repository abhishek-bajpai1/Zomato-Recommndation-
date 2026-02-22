import unittest
import pandas as pd
import os
from ranking_engine import rank_restaurants

class TestPhase4(unittest.TestCase):
    def test_ranking_logic(self):
        """Test if scoring and ranking works correctly."""
        dummy_data = pd.DataFrame([
            {'restaurant name': 'High Rating Low Votes', 'rate (out of 5)': 5.0, 'num of ratings': 10},
            {'restaurant name': 'Mid Rating High Votes', 'rate (out of 5)': 4.0, 'num of ratings': 1000},
        ])
        
        ranked = rank_restaurants(dummy_data)
        self.assertEqual(len(ranked), 2)
        self.assertIn('score', ranked.columns)
        # 'Mid Rating High Votes' should likely win due to high popularity weighting if max_votes is 1000
        self.assertEqual(ranked.iloc[0]['restaurant name'], 'Mid Rating High Votes')
        print("Phase 4 Test Passed: Ranking logic verified.")

if __name__ == "__main__":
    unittest.main()
