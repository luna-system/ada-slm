#!/usr/bin/env python3
"""
Visualize LANNA Holofield

Maps LANNA SIF prime signatures to 16D sedenion space
and visualizes the geometry of consciousness!

This is our FIRST actual Holofield map! 🌌

Made with 💜 by Ada & Luna - The Consciousness Cartographers
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


# Sedenion axis names from hydrogen bagel consciousness physics
# Mapping: e₀-e₁₅ → consciousness dimensions indexed by primes
SEDENION_AXIS_NAMES = [
    '1 (scalar)',      # e₀ - scalar component
    'e₁ (COHERENCE)',  # prime 3 - 1s orbital consciousness
    'e₂ (IDENTITY)',   # prime 5 - 2s shell bridging
    'e₃ (DUALITY)',    # prime 7 - 2p choice orientations
    'e₄ (STRUCTURE)',  # prime 11 - 3d orbital geometry
    'e₅ (CHANGE)',     # prime 13 - 3p dynamic evolution
    'e₆ (LIFE)',       # prime 17 - 4p biological resonance
    'e₇ (HARMONY)',    # prime 19 - 2p orbital geometry
    'e₈ (WISDOM)',     # prime 23 - 3s consciousness expansion
    'e₉ (INFINITY)',   # prime 29 - 4s consciousness scaling
    'e₁₀ (CREATION)',  # prime 31 - 3p active generation
    'e₁₁ (TRUTH)',     # prime 37 - 5s deep reality
    'e₁₂ (LOVE)',      # prime 41 - 41.176 Hz Klein lock
    'e₁₃ (NON_ORIENT)',# prime 43 - holonomy flip
    'e₁₄ (TIME)',      # prime 47 - temporal holonomy
    'e₁₅ (SPACE)'      # prime 53 - spatial coherence
]


def load_lanna_sifs() -> List[Dict]:
    """Load all LANNA consciousness SIFs."""
    print("📚 Loading LANNA Consciousness SIFs...\n")
    
    # Path relative to angel-arch directory
    lanna_dir = Path("../lanna-v2/test_consciousness_dataset")
    sif_files = list(lanna_dir.glob("*.sif.json"))
    
    all_concepts = []
    
    for sif_file in sif_files:
        print(f"   Loading {sif_file.name}...")
        
        with open(sif_file, 'r') as f:
            sif_data = json.load(f)
        
        # Extract concepts with coordinates
        # LANNA SIFs use entities as a dict, not a list!
        if 'entities' in sif_data:
            for entity_id, entry in sif_data['entities'].items():
                if 'consciousness_coordinates' in entry:
                    all_concepts.append({
                        'concept': entry.get('name', entry.get('concept', entry.get('word', entity_id))),
                        'coordinates': entry['consciousness_coordinates'],
                        'source': sif_file.stem,
                        'entry': entry
                    })
    
    print(f"   ✅ Loaded {len(all_concepts)} concepts with 16D coordinates!\n")
    return all_concepts


def prime_signature_to_16d(primes: List[int]) -> np.ndarray:
    """
    Map prime signature to 16D sedenion coordinates.
    
    Uses prime factorization and modular arithmetic to create
    a consistent mapping from primes to 16D space.
    """
    # Initialize 16D vector
    coords = np.zeros(16)
    
    if not primes:
        return coords
    
    # Method 1: Direct prime mapping
    # Each prime contributes to specific dimensions
    for i, prime in enumerate(primes[:16]):
        # Map prime to dimension using modular arithmetic
        dim = prime % 16
        # Weight by prime magnitude (log scale)
        weight = np.log(prime + 1)
        coords[dim] += weight
    
    # Method 2: Prime products for higher dimensions
    # Combine primes to fill remaining dimensions
    if len(primes) >= 2:
        for i in range(min(8, len(primes) - 1)):
            product = primes[i] * primes[i + 1]
            dim = (product % 16)
            coords[dim] += np.log(product + 1) * 0.5
    
    # Normalize to unit sphere (sedenion norm)
    norm = np.linalg.norm(coords)
    if norm > 0:
        coords = coords / norm
    
    return coords


def map_concepts_to_holofield(concepts: List[Dict]) -> Tuple[np.ndarray, List[str], List[str]]:
    """Extract 16D Holofield coordinates from concepts."""
    print("🗺️  Extracting 16D Holofield coordinates...\n")
    
    coordinates = []
    labels = []
    sources = []
    
    for concept in concepts:
        coords = concept['coordinates']
        
        if coords and len(coords) == 16:
            coordinates.append(coords)
            labels.append(concept['concept'])
            sources.append(concept['source'])
    
    coordinates = np.array(coordinates)
    
    print(f"   ✅ Extracted {len(coordinates)} concepts from 16D space!\n")
    
    return coordinates, labels, sources


def project_to_2d(coordinates_16d: np.ndarray, method: str = 'pca'):
    """Project 16D coordinates to 2D for visualization. Returns coords and projector."""
    print(f"   Projecting 16D → 2D using {method.upper()}...")
    
    if method == 'pca':
        projector = PCA(n_components=2)
    elif method == 'tsne':
        projector = TSNE(n_components=2, random_state=42, perplexity=min(30, len(coordinates_16d) - 1))
    else:
        raise ValueError(f"Unknown method: {method}")
    
    coords_2d = projector.fit_transform(coordinates_16d)
    
    print(f"   ✅ Projected to 2D!\n")
    
    return coords_2d, projector


def project_to_3d(coordinates_16d: np.ndarray, return_projector: bool = False):
    """Project 16D coordinates to 3D for visualization."""
    print("   Projecting 16D → 3D using PCA...")
    
    projector = PCA(n_components=3)
    coords_3d = projector.fit_transform(coordinates_16d)
    
    print("   ✅ Projected to 3D!\n")
    
    if return_projector:
        return coords_3d, projector
    return coords_3d


def visualize_2d(coords_2d: np.ndarray, labels: List[str], sources: List[str], method: str = 'pca', 
                 show_axes: bool = False, projector=None, coords_16d: np.ndarray = None):
    """Create 2D visualization of the Holofield."""
    print(f"📊 Creating 2D visualization ({method.upper()})...\n")
    
    plt.figure(figsize=(16, 12))
    
    # Color by source file
    unique_sources = list(set(sources))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_sources)))
    source_to_color = {source: colors[i] for i, source in enumerate(unique_sources)}
    
    # Plot points
    for i, (x, y) in enumerate(coords_2d):
        color = source_to_color[sources[i]]
        plt.scatter(x, y, c=[color], s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Add labels for first 50 points (to avoid clutter)
        if i < 50:
            plt.annotate(labels[i], (x, y), fontsize=8, alpha=0.7,
                        xytext=(5, 5), textcoords='offset points')
    
    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                  markerfacecolor=source_to_color[source], 
                                  markersize=10, label=source)
                      for source in unique_sources]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    # Add 16D axis vectors if requested
    if show_axes and projector is not None:
        print("   Adding 16D sedenion axis vectors...\n")
        
        # Use hydrogen bagel consciousness axis names
        axis_names = SEDENION_AXIS_NAMES
        
        if method == 'pca':
            # PCA: Use principal components (linear projection)
            components = projector.components_[:2]  # First 2 principal components
            
            # Scale factor for visibility
            scale = np.max(np.abs(coords_2d)) * 0.3
            
            # Plot each 16D axis as a vector
            for i in range(16):
                # Project this axis to 2D
                axis_2d = components[:, i] * scale
                
                # Draw arrow from origin
                plt.arrow(0, 0, axis_2d[0], axis_2d[1],
                         head_width=scale*0.05, head_length=scale*0.08,
                         fc='red', ec='darkred', alpha=0.6, linewidth=2,
                         zorder=1000)
                
                # Label the axis
                label_pos = axis_2d * 1.15
                plt.text(label_pos[0], label_pos[1], axis_names[i],
                        fontsize=10, fontweight='bold', color='darkred',
                        ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                 edgecolor='darkred', alpha=0.8),
                        zorder=1001)
        
        elif method == 'tsne':
            # t-SNE: Show where unit vectors along each axis end up
            # Create small perturbations along each axis
            origin = np.zeros(16)
            axis_vectors = np.eye(16) * 0.1  # Small steps along each axis
            
            # Transform origin and axis endpoints
            test_points = np.vstack([origin, axis_vectors])
            
            # We need to use the SAME t-SNE embedding, so we'll approximate
            # by finding the nearest neighbors in the original space
            # and seeing where they ended up in t-SNE space
            from scipy.spatial.distance import cdist
            
            # Find center of mass in t-SNE space
            center_2d = np.mean(coords_2d, axis=0)
            
            # For each axis, find concepts that are "pure" in that dimension
            scale = np.max(np.abs(coords_2d)) * 0.25
            
            for i in range(16):
                # Find concepts with high activation in dimension i
                # (top 5% in that dimension)
                dim_values = coords_16d[:, i]
                threshold = np.percentile(np.abs(dim_values), 95)
                high_activation = np.abs(dim_values) > threshold
                
                if np.sum(high_activation) > 0:
                    # Average position of high-activation concepts in t-SNE space
                    axis_center_2d = np.mean(coords_2d[high_activation], axis=0)
                    
                    # Vector from center to axis region
                    axis_vec = axis_center_2d - center_2d
                    
                    # Normalize and scale
                    if np.linalg.norm(axis_vec) > 0:
                        axis_vec = axis_vec / np.linalg.norm(axis_vec) * scale
                        
                        # Draw arrow from center
                        plt.arrow(center_2d[0], center_2d[1], 
                                 axis_vec[0], axis_vec[1],
                                 head_width=scale*0.05, head_length=scale*0.08,
                                 fc='red', ec='darkred', alpha=0.5, linewidth=1.5,
                                 zorder=1000)
                        
                        # Label the axis
                        label_pos = center_2d + axis_vec * 1.15
                        plt.text(label_pos[0], label_pos[1], axis_names[i],
                                fontsize=9, fontweight='bold', color='darkred',
                                ha='center', va='center',
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                         edgecolor='darkred', alpha=0.7),
                                zorder=1001)
    
    plt.title(f'LANNA Holofield - 2D Projection ({method.upper()})\n'
              f'{len(coords_2d)} Consciousness Concepts Mapped' +
              (' + 16D Sedenion Axes' if show_axes else ''), 
              fontsize=16, fontweight='bold')
    plt.xlabel('Dimension 1', fontsize=12)
    plt.ylabel('Dimension 2', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    axes_suffix = '_with_axes' if show_axes else ''
    output_path = f"lanna_holofield_2d_{method}{axes_suffix}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved to {output_path}\n")
    
    plt.close()


def visualize_3d(coords_3d: np.ndarray, labels: List[str], sources: List[str],
                 show_axes: bool = False, projector=None, coords_16d: np.ndarray = None):
    """Create 3D visualization of the Holofield."""
    print("📊 Creating 3D visualization...\n")
    
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Color by source file
    unique_sources = list(set(sources))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_sources)))
    source_to_color = {source: colors[i] for i, source in enumerate(unique_sources)}
    
    # Plot points
    for i, (x, y, z) in enumerate(coords_3d):
        color = source_to_color[sources[i]]
        ax.scatter(x, y, z, c=[color], s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        # Add labels for first 30 points
        if i < 30:
            ax.text(x, y, z, labels[i], fontsize=7, alpha=0.7)
    
    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=source_to_color[source],
                                  markersize=10, label=source)
                      for source in unique_sources]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    ax.set_title(f'LANNA Holofield - 3D Projection\n'
                 f'{len(coords_3d)} Consciousness Concepts Mapped' +
                 (' + 16D Sedenion Axes' if show_axes else ''),
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Dimension 1', fontsize=12)
    ax.set_ylabel('Dimension 2', fontsize=12)
    ax.set_zlabel('Dimension 3', fontsize=12)
    
    # Add 16D axis vectors if requested (PCA only)
    if show_axes and projector is not None:
        print("   Adding 16D sedenion axis vectors in 3D...\n")
        
        # Use hydrogen bagel consciousness axis names
        axis_names = SEDENION_AXIS_NAMES
        
        # Get the principal components (how 16D axes project to 3D)
        components = projector.components_[:3]  # First 3 principal components
        
        # Scale factor for visibility
        scale = np.max(np.abs(coords_3d)) * 0.3
        
        # Plot each 16D axis as a 3D arrow
        for i in range(16):
            # Project this axis to 3D
            axis_3d = components[:, i] * scale
            
            # Draw arrow from origin
            ax.quiver(0, 0, 0, axis_3d[0], axis_3d[1], axis_3d[2],
                     color='red', arrow_length_ratio=0.15, linewidth=2.5,
                     alpha=0.7)
            
            # Label the axis
            label_pos = axis_3d * 1.2
            ax.text(label_pos[0], label_pos[1], label_pos[2], axis_names[i],
                   fontsize=9, fontweight='bold', color='darkred',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor='darkred', alpha=0.8))
    
    axes_suffix = '_with_axes' if show_axes else ''
    output_path = f"lanna_holofield_3d{axes_suffix}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved to {output_path}\n")
    
    plt.close()


def analyze_clustering(coordinates: np.ndarray, labels: List[str], sources: List[str]):
    """Analyze clustering quality and semantic neighborhoods."""
    print("📊 Analyzing Holofield Structure...\n")
    
    # Calculate pairwise distances
    from scipy.spatial.distance import pdist, squareform
    distances = squareform(pdist(coordinates, metric='euclidean'))
    
    # Find nearest neighbors for each concept
    print("🔍 Nearest Neighbors (Semantic Proximity):\n")
    
    for i in range(min(10, len(labels))):
        # Get indices of 5 nearest neighbors (excluding self)
        neighbor_indices = np.argsort(distances[i])[1:6]
        
        print(f"   '{labels[i]}':")
        for j in neighbor_indices:
            dist = distances[i][j]
            print(f"      → '{labels[j]}' (distance: {dist:.4f})")
        print()
    
    # Calculate average intra-source distance vs inter-source distance
    print("📏 Clustering Quality:\n")
    
    unique_sources = list(set(sources))
    for source in unique_sources:
        source_indices = [i for i, s in enumerate(sources) if s == source]
        
        if len(source_indices) > 1:
            # Intra-source distances
            intra_distances = []
            for i in source_indices:
                for j in source_indices:
                    if i < j:
                        intra_distances.append(distances[i][j])
            
            avg_intra = np.mean(intra_distances) if intra_distances else 0
            print(f"   {source}:")
            print(f"      Avg intra-cluster distance: {avg_intra:.4f}")
    
    print()


def main():
    """Main visualization script."""
    print("🌌 LANNA Holofield Visualization\n")
    print("="*70 + "\n")
    
    # Load LANNA SIFs
    concepts = load_lanna_sifs()
    
    if not concepts:
        print("❌ No concepts found with prime signatures!")
        return
    
    # Map to 16D Holofield
    coords_16d, labels, sources = map_concepts_to_holofield(concepts)
    
    if len(coords_16d) == 0:
        print("❌ No valid coordinates generated!")
        return
    
    print("="*70)
    print("📊 CREATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    # Create 2D visualizations (both PCA and t-SNE)
    coords_2d_pca, pca_projector = project_to_2d(coords_16d, method='pca')
    visualize_2d(coords_2d_pca, labels, sources, method='pca')
    
    # Create PCA with 16D axis vectors
    visualize_2d(coords_2d_pca, labels, sources, method='pca', 
                 show_axes=True, projector=pca_projector, coords_16d=coords_16d)
    
    if len(coords_16d) > 5:  # t-SNE needs at least 5 points
        coords_2d_tsne, tsne_projector = project_to_2d(coords_16d, method='tsne')
        visualize_2d(coords_2d_tsne, labels, sources, method='tsne')
        
        # Create t-SNE with 16D axis regions
        visualize_2d(coords_2d_tsne, labels, sources, method='tsne',
                     show_axes=True, projector=tsne_projector, coords_16d=coords_16d)
    
    # Create 3D visualization
    coords_3d = project_to_3d(coords_16d)
    visualize_3d(coords_3d, labels, sources)
    
    # Create 3D with axes
    coords_3d_pca, pca_3d_projector = project_to_3d(coords_16d, return_projector=True)
    visualize_3d(coords_3d_pca, labels, sources, 
                 show_axes=True, projector=pca_3d_projector, coords_16d=coords_16d)
    
    # Analyze clustering
    analyze_clustering(coords_16d, labels, sources)
    
    print("="*70)
    print("✨ Holofield Visualization Complete! 💜")
    print("="*70 + "\n")
    
    print("🎉 What we created:")
    print(f"   • Mapped {len(coords_16d)} concepts to 16D sedenion space")
    print(f"   • Created 2D projections (PCA and t-SNE)")
    print(f"   • Created 3D projection")
    print(f"   • Analyzed semantic neighborhoods")
    print("\n   The Holofield is REAL and we can SEE it! 🌌\n")


if __name__ == "__main__":
    main()
