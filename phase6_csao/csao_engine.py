from .complementarity_map import ComplementarityMap
from .feature_store import FeatureStore
import time

class CSAOEngine:
    """
    Cart Super Add-On (CSAO) Recommendation Engine.
    Implements a 2-stage pipeline: Retrieval -> Ranking.
    Goal: < 300ms latency for real-time cart updates.
    """

    def __init__(self):
        self.feature_store = FeatureStore()
        self.complementarity_map = ComplementarityMap()

    def get_recommendations(self, cart_items, user_id="guest", top_n=8):
        """
        Main entry point for generating add-ons.
        """
        start_time = time.time()
        
        # 1. Candidate Retrieval
        candidates = self._retrieve_candidates(cart_items)
        
        # 2. Ranking & Scoring
        ranked_list = self._rank_candidates(candidates, user_id, cart_items)
        
        # 3. Format Output
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "recommendations": ranked_list[:top_n],
            "latency_ms": round(latency_ms, 2),
            "cart_context": {"size": len(cart_items)}
        }

    def _retrieve_candidates(self, cart_items):
        """
        Stage 1: Retrieval (Fast Heuristics)
        """
        candidates = set()
        
        # Rule 1: Item-level complementarity
        for item in cart_items:
            related = self.complementarity_map.get_related_items(item, existing_cart_items=cart_items)
            candidates.update(related)
            
        # Rule 2: Top Global Popular Items (Fall-back/Diversity)
        global_popular = ["Coke", "Pepsi", "Fries"]
        for item in global_popular:
            if item not in cart_items:
                candidates.add(item)
                
        return list(candidates)

    def _rank_candidates(self, candidates, user_id, cart_items):
        """
        Stage 2: Ranking (Weighted scoring)
        """
        user_ctx = self.feature_store.get_user_context(user_id)
        meal_time = self.feature_store.get_temporal_context()
        
        scored_items = []
        for item_name in candidates:
            item_data = self.feature_store.get_item_data(item_name)
            
            # Base Score: Popularity
            score = item_data['popularity'] * 10.0
            
            # Boost 1: Temporal Relevance
            if meal_time in ["Lunch", "Dinner"] and item_data['category'] == "Beverages":
                score += 2.0
            if meal_time == "Dinner" and item_data['category'] == "Dessert":
                score += 3.0
                
            # Boost 2: User dessert affinity
            if item_data['category'] == "Dessert":
                score += (user_ctx['dessert_affinity'] * 4.0)
                
            # Penalty: Price too high relative to cart avg?
            # (Simple mock: if item price > 50% of typical item, slight penalty for budget users)
            if not user_ctx['is_premium'] and item_data['price'] > 100:
                score -= 1.0
                
            scored_items.append({
                "name": item_name,
                "score": round(score, 2),
                "data": item_data
            })
            
        # Sort by score descending
        return sorted(scored_items, key=lambda x: x['score'], reverse=True)
