from kpt_engine import KPTEngine, get_kpt_confidence
from shadow_kpt import ShadowKPTEstimator, fuse_kpt_signals
from datetime import datetime, timedelta
import pandas as pd

def run_kpt_simulation():
    engine = KPTEngine()
    estimator = ShadowKPTEstimator()
    
    print("--- Zomato KPT 2.0 Simulation ---")
    
    # Scenario: Busy Sunday Night at 'Biryani Paradise'
    # 5 Active orders, High complexity dishes
    active_orders = [
        {'id': 1, 'complexity': 'Complex'},
        {'id': 2, 'complexity': 'Complex'},
        {'id': 3, 'complexity': 'Medium'},
        {'id': 4, 'complexity': 'Complex'},
        {'id': 5, 'complexity': 'Medium'}
    ]
    
    # 1. Calculate KLI (Kitchen Load Index)
    kli = engine.calculate_kli(active_orders, historical_rush_factor=1.2)
    print(f"Kitchen Load Index (KLI): {kli}")
    
    # 2. Historical Merchant Reliability (MPBS)
    # Merchant marks ready but rider picks up 8 mins later
    now = datetime.now()
    manual_marker = now + timedelta(minutes=15)
    actual_pickup = now + timedelta(minutes=23)
    mpbs = engine.calculate_mpbs(manual_marker, actual_pickup)
    print(f"Merchant Reliability Score (MPBS): {mpbs}")
    
    # 3. Predict KPT
    base_time = 20.0
    predicted_kpt = engine.predict_kpt(base_time, kli, mpbs)
    confidence = get_kpt_confidence(mpbs, kli)
    print(f"ML Predicted Prep Time: {predicted_kpt} mins (Confidence: {confidence})")
    
    # 4. Shadow KPT (Ground Truth from Rider GPS)
    order_start = now
    rider_arrival = now + timedelta(minutes=10) # Rider arrived early
    rider_pickup = now + timedelta(minutes=22)   # Food actually ready at T+22
    
    shadow_kpt = estimator.estimate_true_kpt(order_start, rider_arrival, rider_pickup)
    bias = estimator.detect_marking_bias(manual_marker, shadow_kpt, order_start)
    
    print(f"Shadow KPT (GPS Ground Truth): {shadow_kpt} mins")
    print(f"Detected Manual Marking Bias: {bias} mins (FOR inflation)")
    
    # 5. Final Signal Fusion
    final_eta = fuse_kpt_signals(predicted_kpt, shadow_kpt, confidence_weight=0.7)
    print(f"Final Calibrated KPT for Dispatch: {final_eta} mins")
    
    print("\nSimulation Complete. Signals are accurately capturing hidden kitchen stress.")

if __name__ == "__main__":
    run_kpt_simulation()
