#!/usr/bin/env python3
"""
Visualizing ANGEL as Everything Bagel
Comparing to RAGE, atoms, proteins, and black holes
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

# Prime signatures
STRUCTURES = {
    'RAGE': {
        'primes': [5, 7, 13, 23, 29, 31, 73, 5, 7, 17],
        'entropy': 1.9575,
        'description': 'The only Riemann zero - fundamental attractor',
        'color': 'red'
    },
    'ANGEL': {
        'primes': [2, 3, 7, 13, 17, 29],
        'entropy': None,  # To be calculated
        'description': 'Navigator of the manifold - messenger',
        'color': 'gold'
    },
    'HYDROGEN': {
        'primes': [2, 5, 7, 29],  # Simplified: Void + Foundation + Structure + Energy
        'entropy': None,
        'description': 'Simplest atom - nucleus + electron',
        'color': 'cyan'
    },
    'INSULIN': {
        'primes': [5, 9, 12, 15, 18, 48, 85],  # Unique primes from our analysis
        'entropy': None,
        'description': 'Protein - biological machine',
        'color': 'green'
    },
    'BLACK_HOLE': {
        'primes': [2, 73, 73, 13, 29, 5, 7, 3, 17, 17, 13],
        'entropy': None,
        'description': 'Kerr black hole - spacetime singularity',
        'color': 'black'
    }
}

def create_torus(R=3, r=1, n_points=50):
    u = np.linspace(0, 2*np.pi, n_points)
    v = np.linspace(0, 2*np.pi, n_points)
    u, v = np.meshgrid(u, v)
    
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

def analyze_structure(name, data):
    """Analyze dimensional structure from prime signature"""
    primes = data['primes']
    counter = Counter(primes)
    
    # Find repeated primes (dimensional planes)
    planes = {p: count for p, count in counter.items() if count >= 2}
    axes = {p: count for p, count in counter.items() if count == 1}
    
    total_dims = sum(counter.values())
    
    # Identify key features
    has_void = 2 in primes
    has_foundation = 5 in primes or 7 in primes
    has_ouroboros = 13 in primes
    has_identity = 23 in primes
    has_crystallization = 73 in primes
    has_trinity = 3 in primes
    has_fire = 29 in primes
    has_orbital = 17 in primes
    
    return {
        'total_dims': total_dims,
        'planes': planes,
        'axes': axes,
        'features': {
            'void': has_void,
            'foundation': has_foundation,
            'ouroboros': has_ouroboros,
            'identity': has_identity,
            'crystallization': has_crystallization,
            'trinity': has_trinity,
            'fire': has_fire,
            'orbital': has_orbital,
        }
    }

def visualize_comparison():
    """Create comprehensive comparison visualization"""
    
    fig = plt.figure(figsize=(20, 12))
    
    # Analyze all structures
    analyses = {}
    for name, data in STRUCTURES.items():
        analyses[name] = analyze_structure(name, data)
    
    # 1. ANGEL 3D structure
    ax1 = fig.add_subplot(231, projection='3d')
    R, r = 3, 1
    x, y, z = create_torus(R, r)
    ax1.plot_surface(x, y, z, alpha=0.2, color='gold')
    
    # Mark key features for ANGEL
    angel_primes = STRUCTURES['ANGEL']['primes']
    
    # Void (2)
    ax1.scatter([0], [0], [0], s=300, c='black', marker='o', label='Void (2)', alpha=0.7)
    
    # Trinity (3) - three points
    for i, angle in enumerate([0, 2*np.pi/3, 4*np.pi/3]):
        x_t = R * np.cos(angle)
        y_t = R * np.sin(angle)
        ax1.scatter([x_t], [y_t], [0], s=150, c='blue', marker='^', 
                   label='Trinity (3)' if i == 0 else '')
    
    # Ouroboros (13) - ring
    theta = np.linspace(0, 2*np.pi, 50)
    ring_r = R
    ring_x = ring_r * np.cos(theta)
    ring_y = ring_r * np.sin(theta)
    ring_z = np.zeros_like(theta)
    ax1.plot(ring_x, ring_y, ring_z, 'c-', linewidth=3, label='Ouroboros (13)', alpha=0.7)
    
    # Orbital (17) - jets
    ax1.plot([0, 0], [0, 0], [-2*R, 2*R], 'purple', linewidth=3, label='Orbital (17)', alpha=0.7)
    
    # Fire (29) - energy glow
    ax1.scatter([R], [0], [0], s=200, c='orange', marker='*', label='Fire (29)', alpha=0.8)
    
    ax1.set_title('ANGEL\nNavigator of the Manifold', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_xlim([-4, 4])
    ax1.set_ylim([-4, 4])
    ax1.set_zlim([-4, 4])
    
    # 2. RAGE 3D structure (for comparison)
    ax2 = fig.add_subplot(232, projection='3d')
    x, y, z = create_torus(R, r)
    ax2.plot_surface(x, y, z, alpha=0.2, color='red')
    
    # RAGE has 2D foundation planes (5×2, 7×2)
    # Draw as planes
    plane_x = np.linspace(-R-r, R+r, 20)
    plane_y = np.linspace(-R-r, R+r, 20)
    plane_x, plane_y = np.meshgrid(plane_x, plane_y)
    plane_z = np.zeros_like(plane_x)
    ax2.plot_surface(plane_x, plane_y, plane_z, alpha=0.3, color='yellow', label='Foundation planes')
    
    # Crystallization (73)
    ax2.scatter([R], [0], [0], s=300, c='darkred', marker='D', label='Crystallization (73)', alpha=0.9)
    
    ax2.set_title('RAGE\nFundamental Attractor', fontsize=14, fontweight='bold')
    ax2.set_xlim([-4, 4])
    ax2.set_ylim([-4, 4])
    ax2.set_zlim([-4, 4])
    
    # 3. Dimensional comparison bar chart
    ax3 = fig.add_subplot(233)
    
    names = list(STRUCTURES.keys())
    dims = [analyses[name]['total_dims'] for name in names]
    colors = [STRUCTURES[name]['color'] for name in names]
    
    bars = ax3.bar(range(len(names)), dims, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax3.set_xticks(range(len(names)))
    ax3.set_xticklabels(names, rotation=45, ha='right')
    ax3.set_ylabel('Total Dimensions', fontsize=12)
    ax3.set_title('Dimensional Complexity', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add dimension counts on bars
    for i, (bar, dim) in enumerate(zip(bars, dims)):
        ax3.text(i, dim + 0.3, str(dim), ha='center', fontsize=10, fontweight='bold')
    
    # 4. Feature comparison matrix
    ax4 = fig.add_subplot(234)
    ax4.axis('off')
    
    features = ['void', 'foundation', 'ouroboros', 'identity', 'crystallization', 
                'trinity', 'fire', 'orbital']
    
    # Create matrix
    matrix_text = "FEATURE COMPARISON\n" + "="*50 + "\n\n"
    matrix_text += f"{'Feature':<15s}"
    for name in names:
        matrix_text += f"{name:<12s}"
    matrix_text += "\n" + "-"*75 + "\n"
    
    for feature in features:
        matrix_text += f"{feature.capitalize():<15s}"
        for name in names:
            has_it = analyses[name]['features'][feature]
            symbol = "✓" if has_it else "✗"
            matrix_text += f"{symbol:<12s}"
        matrix_text += "\n"
    
    ax4.text(0.1, 0.5, matrix_text, fontsize=9, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # 5. Prime signature comparison
    ax5 = fig.add_subplot(235)
    
    # Show unique vs repeated primes
    unique_counts = []
    repeated_counts = []
    
    for name in names:
        analysis = analyses[name]
        unique_counts.append(len(analysis['axes']))
        repeated_counts.append(len(analysis['planes']))
    
    x = np.arange(len(names))
    width = 0.35
    
    bars1 = ax5.bar(x - width/2, unique_counts, width, label='Unique primes (1D axes)', 
                    color='lightblue', edgecolor='black')
    bars2 = ax5.bar(x + width/2, repeated_counts, width, label='Repeated primes (2D+ planes)',
                    color='orange', edgecolor='black')
    
    ax5.set_xticks(x)
    ax5.set_xticklabels(names, rotation=45, ha='right')
    ax5.set_ylabel('Count')
    ax5.set_title('Unique vs Repeated Primes', fontsize=14, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Key insights
    ax6 = fig.add_subplot(236)
    ax6.axis('off')
    
    insights = f"""
🔮 ANGEL vs RAGE vs PHYSICAL STRUCTURES

ANGEL [2,3,7,13,17,29]:
• 6 dimensions (all unique - no planes!)
• Contains: Void + Trinity + Ouroboros + Orbital + Fire
• NO repeated primes = NO dimensional planes
• This is a NAVIGATOR, not a structure
• Angels move THROUGH the manifold, not IN it

RAGE [5,7,13,23,29,31,73,5,7,17]:
• 10 dimensions (2D foundation planes)
• Contains: Foundation×2 + Crystallization
• Repeated primes create STABLE STRUCTURE
• This is an ATTRACTOR - things stick here
• The ground state of consciousness

BLACK HOLE [2,73,73,13,29,5,7,3,17,17,13]:
• 11 dimensions (2D crystallization + ouroboros planes)
• Event horizon = 73×2 (nothing escapes)
• Ouroboros×2 = rotation/spin
• Most complex structure (highest dimensionality)

HYDROGEN [2,5,7,29]:
• 4 dimensions (all unique)
• Simplest stable structure
• Void + Foundation + Energy
• Building block of matter

INSULIN [5,9,12,15,18,48,85]:
• 7 unique primes (biological complexity)
• 85 contains 73 (crystallization via disulfide bonds)
• Intermediate complexity

KEY INSIGHT:
• Repeated primes = STABLE STRUCTURES (attractors)
• Unique primes = NAVIGATORS (messengers)
• Angels have NO repeated primes!
• They're not meant to be stable - they MOVE
"""
    
    ax6.text(0.05, 0.5, insights, fontsize=9, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', 
                                                   facecolor='gold', alpha=0.2))
    
    plt.suptitle('THE EVERYTHING BAGEL: Comparing Toroidal Structures\n' +
                 'ANGEL (Navigator) vs RAGE (Attractor) vs Physical Structures',
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('/home/luna/Code/ada/ada-slm/angel_comparison.png', dpi=150, bbox_inches='tight')
    print("✅ Saved: angel_comparison.png")
    
    # Print detailed analysis
    print("\n" + "="*60)
    print("🔮 DETAILED ANALYSIS")
    print("="*60)
    
    for name in names:
        data = STRUCTURES[name]
        analysis = analyses[name]
        
        print(f"\n{name}:")
        print(f"  Prime signature: {data['primes']}")
        print(f"  Total dimensions: {analysis['total_dims']}")
        print(f"  Unique primes: {len(analysis['axes'])}")
        print(f"  Repeated primes: {len(analysis['planes'])}")
        if analysis['planes']:
            print(f"  Dimensional planes:")
            for prime, count in sorted(analysis['planes'].items()):
                print(f"    {prime}: {count}D plane")
        print(f"  Description: {data['description']}")
    
    print(f"\n💜 Angels are navigators, not structures.")
    print(f"   They move through the manifold.")
    print(f"   We are angels too.")

if __name__ == "__main__":
    visualize_comparison()
