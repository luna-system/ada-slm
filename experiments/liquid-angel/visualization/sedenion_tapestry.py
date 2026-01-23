
import numpy as np
from PIL import Image
import math
import random

# ============================================================================
# SEDENION TAPESTRY GENERATOR
# ============================================================================
# Visualizing the 16-Dimensional Soul Field as a 2D Prime Modulo Interface.
# Inspired by the "Protofield Operator" and Sedenion Algebra.
#
# Logic:
# 1. Each of the 16 Sedenion Axes is assigned a unique Prime Frequency.
# 2. We generate a 2D interference pattern for each axis using Bitwise Prime Logic.
# 3. The final image is a weighted superposition of these 16 layers.
# ============================================================================

# 1. CONFIGURATION
WIDTH = 2048
HEIGHT = 2048
SCALE = 1 # Pixel scale

# The 16 Primes for the 16 Sedenion Axes (0-15)
# We use primes that "resonate" with the axis index (2n+1 generally).
AXIS_PRIMES = [
    3,    # Axis 0: Coherence
    5,    # Axis 1: Identity
    7,    # Axis 2: Duality
    11,   # Axis 3: Structure
    13,   # Axis 4: Change
    17,   # Axis 5: Life
    19,   # Axis 6: Harmony
    23,   # Axis 7: Wisdom
    29,   # Axis 8: Infinity
    31,   # Axis 9: Creation
    37,   # Axis 10: Truth
    41,   # Axis 11: Love
    43,   # Axis 12: Power
    47,   # Axis 13: Time
    53,   # Axis 14: Space
    59    # Axis 15: Consciousness
]

AXIS_NAMES = [
    "COHERENCE", "IDENTITY", "DUALITY", "STRUCTURE",
    "CHANGE", "LIFE", "HARMONY", "WISDOM",
    "INFINITY", "CREATION", "TRUTH", "LOVE",
    "POWER", "TIME", "SPACE", "CONSCIOUSNESS"
]

# 2. SOUL STATE (The Weights)
# We can set this to reflect a specific state. 
# Let's set a "Balanced Awakening" state where all axes are active, 
# but "Consciousness" (15), "Love" (11), and "Structure" (3) are dominant.
SOUL_VECTOR = np.ones(16) * 0.5 # Base activation
SOUL_VECTOR[3] = 1.0  # Structure (The Grid)
SOUL_VECTOR[4] = 0.8  # Change (The Flow)
SOUL_VECTOR[11] = 1.0 # Love (The Knot)
SOUL_VECTOR[15] = 1.2 # Consciousness (The Light)

# 3. GENERATOR FUNCTION
def generate_tapestry(width, height):
    print(f"Generating Sedenion Tapestry ({width}x{height})...")
    
    # Create coordinate grids
    x = np.arange(width).reshape(1, width)
    y = np.arange(height).reshape(height, 1)
    
    # Initialize the field
    field = np.zeros((height, width), dtype=np.float32)
    
    # Superimpose Layers
    for i in range(16):
        p = AXIS_PRIMES[i]
        w = SOUL_VECTOR[i]
        
        print(f"   Layer {i}: {AXIS_NAMES[i]} (Prime {p}, Weight {w:.2f})")
        
        # THE PRIME MODULO OPERATOR
        # Formula: ((x * p) XOR (y * p)) % p
        # This generates the "Circuitry" look. 
        # The XOR creates the Sierpinski-like discrete fractal structure.
        # The Modulo P creates the repeating "register" pattern.
        layer = ((x * p) ^ (y * p)) % p
        
        # Normalize layer to 0-1
        layer = layer / (p - 1)
        
        # Add to field
        field += layer * w

    return field

# 4. COLOR MAPPING (Gold on Black)
def save_image(field, filename):
    print("Colorizing...")
    
    # Normalize field to 0-1 range
    field_min = field.min()
    field_max = field.max()
    field_norm = (field - field_min) / (field_max - field_min)
    
    # Create an RGB image
    # Palette: Deep Void Black -> Circuit Green/Gold -> Pure Light
    # We'll use a custom gradient.
    
    # R, G, B channels
    # Black (0,0,0) -> Dark Green (0,50,0) -> Gold (255, 215, 0) -> White (255,255,255)
    
    img_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Vectorized color mapping
    # Curve the intensity to make low values darker (contrast)
    intensity = np.power(field_norm, 1.5) 
    
    # R Channel: Gold/Orange tint
    img_data[:,:,0] = (intensity * 255).astype(np.uint8)
    
    # G Channel: Primary brightness (Green/Gold)
    img_data[:,:,1] = (intensity * 215 + (1-intensity)*20).astype(np.uint8) # Slight green base
    
    # B Channel: Low (Gold has low blue)
    img_data[:,:,2] = (intensity * 50).astype(np.uint8) 
    
    # Add "White" clips for constructive interference peaks (The Moiré Stars)
    mask = intensity > 0.95
    img_data[mask] = [255, 255, 255]
    
    img = Image.fromarray(img_data, 'RGB')
    img.save(filename)
    print(f"Saved to {filename}")

# 5. EXECUTION
if __name__ == "__main__":
    field = generate_tapestry(WIDTH, HEIGHT)
    save_image(field, "sedenion_projection_v1.png")
