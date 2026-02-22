import unittest
import pandas as pd
import os
from llm_engine import RecommendationEngine
from dotenv import load_dotenv

load_dotenv()

class TestPhase3(unittest.TestCase):
    def test_llm_integration(self):
        """Integration test for Groq LLM."""
        if not os.getenv("GROQ_API_KEY"):
            self.skipTest("GROQ_API_KEY not found in environment.")
            
        engine = RecommendationEngine()
        dummy_data = pd.DataFrame([{
            'name': 'Empire Restaurant',
            'location': 'Koramangala',
            'cuisines': 'North Indian, Kebab',
            'rate': '4.1/5',
            'approx_cost(for two people)': '700'
        }])
        
        result = engine.get_recommendations("I'm looking for North Indian food in Koramangala", dummy_data)
        self.assertIsNotNone(result)
        self.assertNotIn("Error", result)
        print("Phase 3 Integration Test Passed: LLM returned recommendations.")
        print("-" * 30)
        print(result)

if __name__ == "__main__":
    unittest.main()
