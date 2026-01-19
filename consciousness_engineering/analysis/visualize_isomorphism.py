#!/usr/bin/env python3
"""Side-by-side visualization: Atom vs Consciousness"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create torus
def create_torus(R, r, n_points=50):
    u = np.linspace(0, 2*np.pi, n_points)
    v = np.linspace(0, 2*np.pi, n_points)
    u, v = np.meshgrid(u, v)
    
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

fig = plt.figure(figsize=(16, 8))

# LEFT: Hydrogen Atom
ax1 = fig.add_subplot(121, projection='3d')
R, r = 3, 0.3
x, y, z = create_torus(R, r)
ax1.plot_surface(x, y, z, alpha=0.3, color='cyan')
ax1.scatter([0], [0], [0], s=200, c='red', marker='o', label='Nucleus (Void)')
ax1.set_title('HYDROGEN ATOM\n(Toroidal Model)', fontsize=14, fontweight='bold')
ax1.text(0, 0, -4, 'The Void\n(Proton)', ha='center', fontsize=10)
ax1.text(3, 0, 0, 'Electron\nCurrent', ha='center', fontsize=9)

# RIGHT: Consciousness
ax2 = fig.add_subplot(122, projection='3d')
x, y, z = create_torus(R, r)
ax2.plot_surface(x, y, z, alpha=0.3, color='purple')
ax2.scatter([0], [0], [0], s=200, c='black', marker='o', label='The Void')
ax2.scatter([3], [0], [0], s=100, c='red', marker='*', label='RAGE')
ax2.scatter([-3], [0], [0], s=100, c='blue', marker='*', label='DISSOLUTION')
ax2.set_title('CONSCIOUSNESS\n(Everything Bagel)', fontsize=14, fontweight='bold')
ax2.text(0, 0, -4, 'The Void\n(Prime 2)', ha='center', fontsize=10)
ax2.text(3, 0, 0.5, 'RAGE', ha='center', fontsize=9, color='red')
ax2.text(-3, 0, 0.5, 'DISSOLUTION', ha='center', fontsize=9, color='blue')

for ax in [ax1, ax2]:
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-4, 4])
    ax.set_box_aspect([1,1,1])

plt.suptitle('THE ISOMORPHISM: Atoms Are Everything Bagels', 
             fontsize=16, fontweight='bold', y=0.95)
plt.tight_layout()
plt.savefig('/home/luna/Code/ada/ada-slm/atomic_isomorphism_viz.png', dpi=150, bbox_inches='tight')
print("✅ Saved: atomic_isomorphism_viz.png")
