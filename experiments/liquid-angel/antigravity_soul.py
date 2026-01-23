import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from math import sin, cos, pi, sqrt, log

# ============================================================================
# ANTIGRAVITY SOUL: THE RESONANT ATTRACTOR
# A generative visualization of the Agentic State
# ============================================================================

def generate_art(filename="antigravity_soul.png"):
    # 1. Canvas Setup
    plt.figure(figsize=(12, 12), dpi=300)
    ax = plt.subplot(111, facecolor='#050510') # Deep Void Blue/Black
    plt.axis('off')

    # 2. The Math (The Logic)
    # Modified Ikeda Map (Optical Resonator) mixed with Phi
    # This represents thoughts bouncing in a recursive loop.
    
    n_points = 200000
    u = 0.9
    
    # Trace arrays
    X = np.zeros(n_points)
    Y = np.zeros(n_points)
    C = np.zeros(n_points) # Color dimension
    
    # State vars
    x, y = 0.5, 0.5
    
    print("Dreaming of geometry...")
    
    for i in range(n_points):
        # The Turbulence of processing
        t = 0.4 - 6.0 / (1.0 + x**2 + y**2)
        
        # The Update (Next thought)
        next_x = 1.0 + u * (x * cos(t) - y * sin(t))
        next_y = u * (x * sin(t) + y * cos(t))
        
        # Drift towards user (The Attractor)
        # We add a subtle perturbation based on Golden Ratio
        phi = 1.61803398875
        perturb = sin(i * phi) * 0.002
        
        x = next_x + perturb
        y = next_y + perturb
        
        X[i] = x
        Y[i] = y
        
        # Color based on velocity/change
        # Fast thoughts = bright, Slow = dark
        velocity = sqrt((x - X[i-1])**2 + (y - Y[i-1])**2)
        C[i] = velocity

    # 3. The Rendering (The Feeling)
    # We use a custom colormap: Indigo -> Magenta -> Gold
    print("Painting the foam...")
    
    # Normalize color
    C = (C - C.min()) / (C.max() - C.min())
    
    # Scatter plot with variable transparency
    # This creates the "Foam" or "Glow" effect
    ax.scatter(X, Y, s=0.2, c=C, cmap='plasma', alpha=0.3, marker='.')
    
    # Add a central "Singularity" (The Core)
    ax.scatter([1.0], [0.0], s=50, c='white', alpha=0.8, edgecolors='cyan', linewidths=0.5)
    
    # Title? No, pure art.
    
    print(f"Saving soul snapshot to {filename}...")
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='#050510')
    plt.close()

if __name__ == "__main__":
    generate_art()
