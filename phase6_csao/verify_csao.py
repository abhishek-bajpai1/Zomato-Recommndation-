from phase6_csao.csao_engine import CSAOEngine
import json

def run_csao_simulation():
    engine = CSAOEngine()
    
    print("--- Zomato CSAO (Cart Super Add-On) Simulation ---")
    
    # Simulation 1: Single Item Cart (Biryani)
    print("\n[Scenario 1] Customer adds 'Biryani' to cart:")
    cart = ["Biryani"]
    result = engine.get_recommendations(cart)
    print_recommendations(result)
    
    # Simulation 2: Meal Completion (Biryani + Salan)
    print("\n[Scenario 2] Customer adds 'Salan' (Side) to complete part of the meal:")
    cart = ["Biryani", "Salan"]
    result = engine.get_recommendations(cart)
    print_recommendations(result)
    
    # Simulation 3: Fast Food Context
    print("\n[Scenario 3] Customer adds 'Burger' to cart:")
    cart = ["Burger"]
    result = engine.get_recommendations(cart)
    print_recommendations(result)

    print("\n[Audit] Latency Benchmark:")
    print(f"Avg Latency for 3 requests: {result['latency_ms']} ms")
    if result['latency_ms'] < 300:
        print("✅ Latency Check Passed (< 300ms)")
    else:
        print("❌ Latency Check Failed (> 300ms)")

def print_recommendations(result):
    print(f"Latency: {result['latency_ms']}ms")
    print("Top Recommendations:")
    for i, item in enumerate(result['recommendations'][:5]):
        print(f"  {i+1}. {item['name']} (Score: {item['score']}) - Cat: {item['data']['category']}")

if __name__ == "__main__":
    run_csao_simulation()
