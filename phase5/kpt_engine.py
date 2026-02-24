import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class KPTEngine:
    """
    Electronic Engine for predicting Kitchen Prep Time (KPT) using multi-signal inputs.
    Reduces reliance on manual 'Food Ready' (FOR) signals.
    """
    
    def __init__(self):
        # Coefficients based on historical Zomato data patterns
        self.complexity_weights = {
            'Simple': 1.0,     # e.g., Beverages, Snacks
            'Medium': 1.5,     # e.g., Fast Food, North Indian
            'Complex': 2.5     # e.g., Fine Dining, Multi-course
        }
        
    def calculate_kli(self, active_orders, historical_rush_factor=1.0):
        """
        Calculates the Kitchen Load Index (KLI).
        KLI = (Sum of active order complexity) * Rush Factor
        """
        if not active_orders:
            return 0.0
            
        total_complexity = sum([self.complexity_weights.get(o.get('complexity', 'Medium'), 1.5) 
                              for o in active_orders])
        
        # Scaling factor: total complexity / total kitchen stations (estimated)
        kli = total_complexity * historical_rush_factor
        return round(kli, 2)

    def calculate_mpbs(self, manual_ready_time, actual_pickup_time):
        """
        Merchant Reliability Score (MPBS).
        Measures the bias between manual markers and reality.
        Positive delta means the merchant marks 'Ready' early (FOR inflation).
        """
        delta = (actual_pickup_time - manual_ready_time).total_seconds() / 60.0
        
        # Reliability score (0 to 1). Higher is better.
        # Penalty for high delta (e.g., marked ready 10 mins before pickup)
        reliability = max(0, 1 - (abs(delta) / 30.0))
        return round(reliability, 2)

    def predict_kpt(self, base_prep_time, kli, mpbs):
        """
        Predicts the finalized KPT using signals.
        Predicted KPT = Base + (KLI adjustment) + (Merchant Bias adjustment)
        """
        # Load impact: +2 mins per KLI unit above 5.0
        load_adjustment = max(0, (kli - 5.0) * 2.0)
        
        # Bias adjustment: If mpbs is low (< 0.7), add buffer based on historical delta
        bias_adjustment = (1 - mpbs) * 10.0
        
        final_kpt = base_prep_time + load_adjustment + bias_adjustment
        return round(final_kpt, 2)

# Global helper for signal confidence
def get_kpt_confidence(mpbs, kli):
    if mpbs > 0.8 and kli < 10:
        return "High"
    elif mpbs < 0.5 or kli > 20:
        return "Low"
    return "Medium"
