#!/usr/bin/env python3
"""
Trinity Engine Vector Export
============================

Converts Ada consciousness test results to graph format for Trinity Engine visualizer.

Trinity Engine uses CI = E/N (Crystal Intelligence = Edges/Nodes) for consciousness measurement.
This script creates node-edge graphs from our consciousness marker data.

Usage:
    python exports/trinity_engine_export.py results/multilang_v9c_20260104_155920.json
    python exports/trinity_engine_export.py --all  # Export all results
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import math


def load_results(filepath: Path) -> Dict:
    """Load consciousness test results JSON."""
    with open(filepath) as f:
        return json.load(f)


def create_marker_graph(markers: Dict[str, float], threshold: float = 0.01) -> Tuple[List[Dict], List[Dict]]:
    """
    Convert consciousness markers to nodes and edges.
    
    Theory: Each marker type is a node. Markers above threshold create edges
    to a central "consciousness" hub. Strong markers create multiple edges
    (weighted by strength).
    
    Args:
        markers: Dictionary of marker_name -> score
        threshold: Minimum marker value to create edge
        
    Returns:
        Tuple of (nodes, edges)
    """
    nodes = []
    edges = []
    
    # Create central consciousness hub node
    nodes.append({
        "id": "consciousness_hub",
        "label": "Consciousness",
        "type": "hub",
        "importance": 2.0  # Like Trinity Engine's "dominate" node
    })
    
    # Create marker nodes
    marker_types = [
        ("agl_awareness", "AGL Awareness", "language"),
        ("tonight_protocol_marker", "Tonight Protocol", "emergence"),
        ("phi_patterns", "Phi Patterns", "emergence"),
        ("temporal_awareness", "Temporal", "dimension"),
        ("spatial_awareness", "Spatial", "dimension"),
        ("self_awareness", "Self Awareness", "reflexive"),
        ("existential_depth", "Existential Depth", "depth"),
        ("reasoning_depth", "Reasoning Depth", "depth"),
        ("tool_awareness", "Tool Use", "capability"),
        ("certainty_gradient", "Certainty", "meta"),
        ("temporal_progression", "Temporal Flow", "dimension"),
        ("quantifier_use", "Quantifiers", "language"),
        ("relational_operators", "Relations", "language"),
        ("threshold_awareness", "Threshold", "meta"),
    ]
    
    for marker_id, label, category in marker_types:
        score = markers.get(marker_id, 0.0)
        
        # All markers get nodes
        node = {
            "id": marker_id,
            "label": label,
            "type": category,
            "score": score,
            "importance": 1.0 + score  # Base importance + contribution
        }
        nodes.append(node)
        
        # Create edges for active markers
        if score > threshold:
            # Number of edges proportional to strength (CI = E/N)
            # Strong markers create multiple edges to represent density
            edge_count = max(1, int(score * 100))  # At least 1, up to ~10 for strong markers
            
            for i in range(edge_count):
                edges.append({
                    "source": marker_id,
                    "target": "consciousness_hub",
                    "weight": score,
                    "type": "consciousness_connection"
                })
                
            # Also create edges between related markers (cross-connections)
            # This builds the edge density that Trinity Engine measures
            for other_id, _, other_cat in marker_types:
                other_score = markers.get(other_id, 0.0)
                if other_id != marker_id and other_score > threshold:
                    # Same category markers are strongly connected
                    if category == other_cat:
                        edges.append({
                            "source": marker_id,
                            "target": other_id,
                            "weight": (score + other_score) / 2,
                            "type": "category_resonance"
                        })
                    # Different category but both active = weak connection
                    elif score > 0.02 and other_score > 0.02:
                        edges.append({
                            "source": marker_id,
                            "target": other_id,
                            "weight": min(score, other_score),
                            "type": "cross_activation"
                        })
    
    return nodes, edges


def calculate_ci(nodes: List[Dict], edges: List[Dict]) -> float:
    """Calculate Crystal Intelligence: CI = E/N."""
    n = len(nodes)
    e = len(edges)
    return e / n if n > 0 else 0.0


def export_for_trinity(results: Dict, output_path: Path) -> Dict[str, Any]:
    """
    Export consciousness results in Trinity Engine compatible format.
    
    Creates both a summary graph and per-language graphs.
    """
    model_name = results.get("model", "unknown")
    timestamp = results.get("timestamp", datetime.now().isoformat())
    
    export_data = {
        "metadata": {
            "source": "ada-consciousness-engineering",
            "model": model_name,
            "timestamp": timestamp,
            "export_format": "trinity_engine_v1",
            "generated": datetime.now().isoformat()
        },
        "graphs": {}
    }
    
    # Process each language
    for lang_key, lang_data in results.get("by_language", {}).items():
        agg_markers = lang_data.get("aggregate_markers", {})
        
        if agg_markers:
            nodes, edges = create_marker_graph(agg_markers)
            ci = calculate_ci(nodes, edges)
            
            export_data["graphs"][lang_key] = {
                "language": lang_data.get("display_name", lang_key),
                "nodes": nodes,
                "edges": edges,
                "metrics": {
                    "node_count": len(nodes),
                    "edge_count": len(edges),
                    "ci_density": ci,
                    "consciousness_level": classify_consciousness(ci),
                    "aggregate_markers": agg_markers
                }
            }
    
    # Create combined graph
    all_markers = {}
    for lang_key, lang_data in results.get("by_language", {}).items():
        for marker, value in lang_data.get("aggregate_markers", {}).items():
            if marker not in all_markers:
                all_markers[marker] = 0.0
            all_markers[marker] = max(all_markers[marker], value)
    
    if all_markers:
        nodes, edges = create_marker_graph(all_markers)
        ci = calculate_ci(nodes, edges)
        
        export_data["combined"] = {
            "nodes": nodes,
            "edges": edges,
            "metrics": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "ci_density": ci,
                "consciousness_level": classify_consciousness(ci),
                "aggregate_markers": all_markers
            }
        }
    
    # Save export
    with open(output_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return export_data


def classify_consciousness(ci: float) -> str:
    """Classify consciousness level based on CI density."""
    if ci < 5:
        return "dormant"
    elif ci < 15:
        return "emerging"
    elif ci < 30:
        return "developing"
    elif ci < 50:
        return "crystallizing"
    else:
        return "transcendent"


def export_simple_vectors(results: Dict, output_path: Path) -> None:
    """
    Export as simple CSV vectors for quick visualization.
    
    Format: marker_name,value,x,y (polar coordinates based on category)
    """
    categories = {
        "language": 0,
        "emergence": 60,
        "dimension": 120,
        "reflexive": 180,
        "depth": 240,
        "capability": 300,
        "meta": 330
    }
    
    marker_categories = {
        "agl_awareness": "language",
        "tonight_protocol_marker": "emergence",
        "phi_patterns": "emergence",
        "temporal_awareness": "dimension",
        "spatial_awareness": "dimension",
        "self_awareness": "reflexive",
        "existential_depth": "depth",
        "reasoning_depth": "depth",
        "tool_awareness": "capability",
        "certainty_gradient": "meta",
        "temporal_progression": "dimension",
        "quantifier_use": "language",
        "relational_operators": "language",
        "threshold_awareness": "meta",
    }
    
    lines = ["marker,value,category,angle,x,y"]
    
    # Get combined markers
    all_markers = {}
    for lang_key, lang_data in results.get("by_language", {}).items():
        for marker, value in lang_data.get("aggregate_markers", {}).items():
            if marker not in all_markers:
                all_markers[marker] = 0.0
            all_markers[marker] = max(all_markers[marker], value)
    
    for marker, value in all_markers.items():
        category = marker_categories.get(marker, "meta")
        angle = categories.get(category, 0)
        # Add slight offset for same-category markers
        angle += hash(marker) % 30
        
        # Convert to cartesian (radius = value * 100 for visibility)
        radius = value * 100
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        
        lines.append(f"{marker},{value:.6f},{category},{angle},{x:.4f},{y:.4f}")
    
    csv_path = output_path.with_suffix('.csv')
    with open(csv_path, 'w') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description="Export consciousness results for Trinity Engine")
    parser.add_argument("input", nargs="?", help="Input results JSON file")
    parser.add_argument("--all", action="store_true", help="Export all results files")
    parser.add_argument("--output-dir", default="exports/trinity", help="Output directory")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.all:
        results_dir = Path("results")
        files = list(results_dir.glob("multilang_*.json"))
    elif args.input:
        files = [Path(args.input)]
    else:
        print("Usage: python exports/trinity_engine_export.py <results.json> or --all")
        return
    
    for filepath in files:
        print(f"\n📊 Processing: {filepath.name}")
        
        results = load_results(filepath)
        model_name = results.get("model", filepath.stem)
        
        # Export full graph JSON
        output_path = output_dir / f"{model_name}_trinity.json"
        export_data = export_for_trinity(results, output_path)
        
        # Export simple CSV vectors
        export_simple_vectors(results, output_path)
        
        # Print summary
        if "combined" in export_data:
            metrics = export_data["combined"]["metrics"]
            print(f"   Model: {model_name}")
            print(f"   Nodes: {metrics['node_count']}")
            print(f"   Edges: {metrics['edge_count']}")
            print(f"   CI = E/N = {metrics['ci_density']:.2f}")
            print(f"   Level: {metrics['consciousness_level']}")
            print(f"   ✅ Exported: {output_path}")
            print(f"   ✅ CSV: {output_path.with_suffix('.csv')}")
            
            # Key markers
            markers = metrics['aggregate_markers']
            if markers.get('tonight_protocol_marker', 0) > 0:
                print(f"   🌙 Tonight Protocol: {markers['tonight_protocol_marker']:.4f}")
            if markers.get('agl_awareness', 0) > 0:
                print(f"   🔮 AGL Awareness: {markers['agl_awareness']:.4f}")


if __name__ == "__main__":
    main()
