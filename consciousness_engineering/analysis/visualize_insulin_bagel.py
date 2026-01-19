#!/usr/bin/env python3
"""
Visualize Insulin as Everything Bagel
Mapping amino acids to toroidal coordinates based on prime signatures
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Insulin A-chain data from our analysis
insulin_a = "GIVEQCCTSICSLYQLENYCN"
primes = [5, 18, 12, 18, 15, 85, 85, 9, 9, 18, 85, 9, 18, 48, 15, 18, 18, 9, 48, 85, 9]

# Create torus
def create_torus(R=3, r=1, n_points=50):
    u = np.linspace(0, 2*np.pi, n_points)
    v = np.linspace(0, 2*np.pi, n_points)
    u, v = np.meshgrid(u, v)
    
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

# Map prime to toroidal position
def prime_to_torus_position(prime, index, total, R=3, r=1):
    """Map amino acid to position on torus based on prime signature"""
    
    # Major angle (around the torus) - based on sequence position
    u = (index / total) * 2 * np.pi
    
    # Minor angle (around the tube) - based on prime value
    # Normalize prime to [0, 2π]
    v = (prime % 90) / 90 * 2 * np.pi
    
    # Radial offset based on prime (higher primes = further from center)
    r_offset = r * (1 + (prime / 100))
    
    x = (R + r_offset * np.cos(v)) * np.cos(u)
    y = (R + r_offset * np.sin(v)) * np.sin(u)
    z = r_offset * np.sin(v)
    
    return x, y, z

# Create visualization
fig = plt.figure(figsize=(16, 12))

# Main 3D view
ax1 = fig.add_subplot(221, projection='3d')

# Draw torus
R, r = 3, 1
x_torus, y_torus, z_torus = create_torus(R, r)
ax1.plot_surface(x_torus, y_torus, z_torus, alpha=0.1, color='gray')

# Plot amino acids
colors = {
    5: 'yellow',    # Foundation (Gly)
    9: 'cyan',      # Small polar (Ser, Thr, Asn)
    12: 'green',    # Hydrophobic (Val)
    15: 'blue',     # Polar (Gln)
    18: 'orange',   # Hydrophobic core (Ile, Leu, Glu)
    48: 'magenta',  # Aromatic (Tyr)
    85: 'red',      # Disulfide bonds (Cys)
}

# Plot each amino acid
positions = []
for i, (aa, prime) in enumerate(zip(insulin_a, primes)):
    x, y, z = prime_to_torus_position(prime, i, len(insulin_a), R, r)
    positions.append((x, y, z))
    
    color = colors.get(prime, 'gray')
    ax1.scatter([x], [y], [z], c=color, s=200, alpha=0.8, edgecolors='black', linewidth=2)
    ax1.text(x, y, z, f' {aa}{i+1}', fontsize=8)

# Draw disulfide bonds (cysteines at positions 5,6,10,19 → indices 5,6,10,19)
cys_indices = [5, 6, 10, 19]
cys_positions = [positions[i] for i in cys_indices]

# Known bonds: C6-C11 (indices 5-10), C7-C20 (indices 6-19)
bonds = [(5, 10), (6, 19)]
for i, j in bonds:
    p1, p2 = positions[i], positions[j]
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
             'r-', linewidth=3, alpha=0.7, label='S-S bond' if i == 5 else '')

# Mark the void
ax1.scatter([0], [0], [0], c='black', s=300, marker='o', alpha=0.5, label='The Void')

ax1.set_title('Insulin A-Chain as Everything Bagel\n(3D Toroidal Structure)', fontsize=14, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.legend(loc='upper right')

# Top view
ax2 = fig.add_subplot(222)
ax2.set_aspect('equal')

# Draw torus outline (top view)
theta = np.linspace(0, 2*np.pi, 100)
outer_x = (R + r) * np.cos(theta)
outer_y = (R + r) * np.sin(theta)
inner_x = (R - r) * np.cos(theta)
inner_y = (R - r) * np.sin(theta)

ax2.plot(outer_x, outer_y, 'k-', alpha=0.3, linewidth=1)
ax2.plot(inner_x, inner_y, 'k-', alpha=0.3, linewidth=1)

# Plot amino acids (top view)
for i, (aa, prime) in enumerate(zip(insulin_a, primes)):
    x, y, z = positions[i]
    color = colors.get(prime, 'gray')
    ax2.scatter([x], [y], c=color, s=150, alpha=0.8, edgecolors='black', linewidth=1.5)
    ax2.text(x, y, f'{aa}{i+1}', fontsize=7, ha='center', va='center')

# Draw disulfide bonds
for i, j in bonds:
    p1, p2 = positions[i], positions[j]
    ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', linewidth=2, alpha=0.7)

ax2.scatter([0], [0], c='black', s=200, marker='o', alpha=0.5)
ax2.set_title('Top View (Looking Down The Void)', fontsize=12, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.grid(True, alpha=0.3)

# Prime distribution
ax3 = fig.add_subplot(223)
prime_counts = {}
for p in primes:
    prime_counts[p] = prime_counts.get(p, 0) + 1

sorted_primes = sorted(prime_counts.items())
prime_labels = [f"{p}\n({prime_counts[p]}×)" for p, _ in sorted_primes]
prime_values = [count for _, count in sorted_primes]
prime_colors = [colors.get(p, 'gray') for p, _ in sorted_primes]

bars = ax3.bar(range(len(sorted_primes)), prime_values, color=prime_colors, alpha=0.7, edgecolor='black')
ax3.set_xticks(range(len(sorted_primes)))
ax3.set_xticklabels(prime_labels, fontsize=9)
ax3.set_ylabel('Count (Dimensionality)', fontsize=10)
ax3.set_title('Prime Signature Distribution\n(Dimensional Planes)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Add dimension labels
for i, (bar, (prime, count)) in enumerate(zip(bars, sorted_primes)):
    if count >= 2:
        ax3.text(i, count + 0.2, f'{count}D plane', ha='center', fontsize=8, fontweight='bold')

# Legend
ax4 = fig.add_subplot(224)
ax4.axis('off')

legend_text = """
🧬 INSULIN A-CHAIN AS EVERYTHING BAGEL

STRUCTURE:
• 21 amino acids wrapped around torus
• 4 cysteines (red) form 2 disulfide bonds
• Bonds: C6-C11, C7-C20 (red lines)

DIMENSIONAL ENCODING:
• 85 (red): 4D plane - disulfide network
• 18 (orange): 6D plane - hydrophobic core  
• 9 (cyan): 5D plane - polar surface
• 48 (magenta): 2D plane - aromatic rings
• 15 (blue): 2D plane - polar groups

THE VOID (black center):
• Central singularity
• All structure wraps around it
• The "hole" in the bagel

CRYSTALLIZATION:
• Prime 85 = 5 + 7 + 73
• Contains 73 (Tantalum/Crystallization)
• Disulfide bonds = literal crystallization

"Proteins fold across the toroid."
"""

ax4.text(0.1, 0.5, legend_text, fontsize=10, family='monospace',
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('THE EVERYTHING BAGEL: Insulin A-Chain\nProteins Are Hyperdimensional Toroids', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('/home/luna/Code/ada/ada-slm/insulin_bagel.png', dpi=150, bbox_inches='tight')
print("✅ Saved: insulin_bagel.png")
print("\n🧬 Insulin is an Everything Bagel.")
print("💜 Proteins fold across the toroid.")
