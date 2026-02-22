import unittest
import os
import pandas as pd
from data_loader import load_zomato_data

class TestPhase1(unittest.TestCase):
    def test_data_loading(self):
        """Test if data is loaded and saved correctly."""
        df = load_zomato_data()
        self.assertIsNotNone(df, "DataFrame should not be None")
        self.assertTrue(os.path.exists("zomato_data.csv"), "zomato_data.csv should be created")
        
        # Basic content check
        df_loaded = pd.read_csv("zomato_data.csv")
        self.assertGreater(len(df_loaded), 0, "Dataset should have records")
        print("Phase 1 Test Passed: Data loaded and verified.")

if __name__ == "__main__":
    unittest.main()
