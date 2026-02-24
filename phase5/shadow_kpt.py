import pandas as pd
from datetime import datetime

class ShadowKPTEstimator:
    """
    Shadow KPT Estimation Engine.
    Uses rider GPS data (dwell time at restaurant) to reverse-calculate 
    the actual 'Ground Truth' prep time, bypassing manual FOR marking bias.
    """
    
    def __init__(self, geofence_radius_meters=100):
        self.geofence_radius = geofence_radius_meters

    def estimate_true_kpt(self, order_start_time, rider_arrival_time, rider_pickup_time):
        """
        Reverse calculates True KPT from rider movements.
        
        True KPT is essentially:
        (Rider Pickup Time - Order Start Time) - (Unproductive Dwell Time)
        
        Wait Time = Rider Pickup Time - max(Order Start Time, Rider Arrival Time)
        """
        # total_time_at_rest = (rider_pickup_time - rider_arrival_time).total_seconds() / 60.0
        
        # If rider arrived AFTER the order started, prep was already ongoing.
        prep_ongoing_duration = max(0, (rider_arrival_time - order_start_time).total_seconds() / 60.0)
        
        # If rider waits, the wait time + ongoing duration = Shadow KPT
        # Note: This assumes rider picks up IMMEDIATELY when food is ready.
        wait_time = max(0, (rider_pickup_time - rider_arrival_time).total_seconds() / 60.0)
        
        shadow_kpt = prep_ongoing_duration + wait_time
        return round(shadow_kpt, 2)

    def detect_marking_bias(self, manual_ready_time, shadow_kpt, order_start_time):
        """
        Calculates the bias delta:
        Bias = Manual FOR Time - (Order Start Time + Shadow KPT)
        Negative bias means merchant MARKED ready after the food was actually picked up (lazy marking).
        Positive bias means merchant MARKED ready before it was actually ready (aggressive marking).
        """
        actual_ready_time = order_start_time + pd.Timedelta(minutes=shadow_kpt)
        bias_minutes = (manual_ready_time - actual_ready_time).total_seconds() / 60.0
        return round(bias_minutes, 2)

# Example helper function for signal fusion
def fuse_kpt_signals(predicted_kpt, shadow_kpt, confidence_weight=0.5):
    """
    Weighted fusion of ML prediction and GPS shadow measurement.
    """
    return round((predicted_kpt * (1 - confidence_weight)) + (shadow_kpt * confidence_weight), 2)
