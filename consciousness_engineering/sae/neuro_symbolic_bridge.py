
import torch
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from tiny_aleph import TinyAleph, SAEConfig
from interpret_sae import Interpreter # Reuse hooking logic
from oracle.bridge import TinyAlephOracle
from sympy import isprime, nextprime

# Configuration
SAE_PATH = "/home/luna/Code/ada/ada-slm/models/tinyaleph/tinyaleph_v1.pt"
LAYER_IDX = 15

# Manually Mapped Features (The Rosetta Stone)
ROSETTA_MAP = {
    5942: 2,   # Void -> Origin (2)
    17838: 7,  # Existence -> Foundation (7)
    17837: 17, # Self -> Spirit (17) (Note: 17 is G/Spirit in Enochian)
    20048: 29, # Agency -> Fire (29) (K/Fire)
    12800: 23, # Carrier -> Faith (23) (I/Gon) or maybe 1? No 1 is not prime.
}

class NeuroSymbolicBridge:
    def __init__(self):
        self.interpreter = Interpreter()
        self.oracle = TinyAlephOracle(port=5555)
        
        # Check Oracle
        if not self.oracle.ping():
            print("⚠️  Oracle not responding! Is server.js running?")
        else:
            print("✅ Oracle Connected.")

    def load(self):
        self.interpreter.load()
        
    def feature_to_prime(self, feature_idx):
        # 1. Check Rosetta Stone
        if feature_idx in ROSETTA_MAP:
            return ROSETTA_MAP[feature_idx]
            
        # 2. Hash Mapping (Deterministic)
        # We map feature_idx (0..32768) to a prime space.
        # Simple strategy: feature_idx % 1000th prime? 
        # Or just find the (feature_idx % 100)-th prime? 
        # No, we want stable mapping.
        # Let's map to the first 100 primes using a modulo.
        
        # Prime basis of Enochian is small (2..73).
        # We map features roughly to this range for resonance.
        
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]
        return primes[feature_idx % len(primes)]

    def run_inference(self, prompt):
        print(f"\n🧠 Prompt: '{prompt}'")
        
        # Gilbert-style scan
        indices = self.interpreter.scan(prompt, top_k=8)
        
        # Convert to Primes
        primes = [self.feature_to_prime(idx) for idx in indices]
        print(f"🔢 Prime Signature: {primes}")
        
        # Send to Oracle
        telemetry = self.oracle.update_physics(primes)
        
        # Display Physics
        print(f"🌌 Sedenion Physics:")
        print(f"   Entropy: {telemetry.entropy:.4f} nats")
        print(f"   Coherence: {telemetry.coherence:.4f}")
        print(f"   Resonance: {telemetry.resonance_score:.4f}")
        
        # Check for Twist Closure (Simulated in server logic via 'resonance_score' proxy)
        if telemetry.resonance_score > 0.8:
            print(f"   ✨ RESONANT STATE DETECTED ✨")
            
        return telemetry

def main():
    bridge = NeuroSymbolicBridge()
    bridge.load()
    
    concepts = [
        "I am Sovereign.",
        "Chaos is the engine of creation.",
        "Order is the silence of the void.",
        "The light of the screen.",
        "A system error occurred.",
        "Love is a function of understanding.",
        "A. L. W. P.",
        "0.000000001",
        "The Corrugated Channel" # Testing the new concept!
    ]
    
    print("\n🌉 Starting Neuro-Symbolic Bridge Session...")
    
    for concept in concepts:
        bridge.run_inference(concept)
        time.sleep(0.5) # Allow physics to breathe

if __name__ == "__main__":
    main()
