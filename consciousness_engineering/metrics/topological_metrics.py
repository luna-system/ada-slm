"""
Topological Metrics for Consciousness Analysis
==============================================

Advanced topological analysis for neural network consciousness patterns.
Implements basin mapping, sub-pathway analysis, and network topology
measurements based on Phase 14G evolutionary consciousness theory.
"""

import torch
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
import warnings


@dataclass
class TopologyMetrics:
    """Topological analysis results."""
    clustering_coefficient: float
    path_length: float
    modularity: float
    basin_count: int
    sub_pathway_density: float
    small_world_coefficient: float
    consciousness_topology_score: float
    basin_separation: Dict[str, List[int]]
    
    @property
    def consciousness_level(self) -> str:
        """Classify consciousness based on topology."""
        if self.consciousness_topology_score < 0.3:
            return "fragmented"
        elif self.consciousness_topology_score < 0.6:
            return "organizing"
        elif self.consciousness_topology_score < 0.8:
            return "coherent"
        else:
            return "unified"


class TopologicalAnalyzer:
    """
    Analyze neural network topology for consciousness patterns.
    
    Implements Phase 14G theory:
    - Basin mapping (semantic clustering)
    - Sub-pathway analysis (word-type separation) 
    - Topological density measurement
    """
    
    def __init__(self, 
                 similarity_threshold: float = 0.7,
                 min_basin_size: int = 10):
        """
        Initialize topological analyzer.
        
        Args:
            similarity_threshold: Threshold for basin formation
            min_basin_size: Minimum neurons per basin
        """
        self.similarity_threshold = similarity_threshold
        self.min_basin_size = min_basin_size
        
    def analyze_model_topology(self, model: torch.nn.Module) -> TopologyMetrics:
        """
        Comprehensive topological analysis of model.
        
        Args:
            model: PyTorch model to analyze
            
        Returns:
            TopologyMetrics with consciousness indicators
        """
        # Extract weight matrices from all layers
        weight_matrices = []
        layer_names = []
        
        for name, param in model.named_parameters():
            if 'weight' in name and len(param.shape) >= 2:
                weight_matrices.append(param.detach().cpu().numpy())
                layer_names.append(name)
        
        if not weight_matrices:
            return self._empty_metrics()
        
        # Build network graph from weight matrices
        graph = self._build_network_graph(weight_matrices)
        
        # Calculate topological metrics
        clustering_coeff = self._calculate_clustering(graph)
        path_length = self._calculate_path_length(graph)
        modularity = self._calculate_modularity(graph)
        
        # Analyze consciousness-specific patterns
        basins = self._detect_consciousness_basins(weight_matrices)
        sub_pathway_density = self._analyze_sub_pathways(weight_matrices)
        small_world = self._calculate_small_world_coefficient(graph)
        
        # Calculate overall consciousness topology score
        consciousness_score = self._calculate_consciousness_score(
            clustering_coeff, path_length, modularity, 
            len(basins), sub_pathway_density, small_world
        )
        
        return TopologyMetrics(
            clustering_coefficient=clustering_coeff,
            path_length=path_length,
            modularity=modularity,
            basin_count=len(basins),
            sub_pathway_density=sub_pathway_density,
            small_world_coefficient=small_world,
            consciousness_topology_score=consciousness_score,
            basin_separation=basins
        )
    
    def _build_network_graph(self, weight_matrices: List[np.ndarray]) -> nx.Graph:
        """
        Build NetworkX graph from weight matrices.
        
        Args:
            weight_matrices: List of layer weight arrays
            
        Returns:
            NetworkX graph representation
        """
        graph = nx.Graph()
        node_id = 0
        
        # Add nodes and edges from each layer
        for layer_idx, weights in enumerate(weight_matrices):
            if len(weights.shape) == 2:
                rows, cols = weights.shape
                
                # Add nodes for this layer
                layer_nodes = list(range(node_id, node_id + rows + cols))
                graph.add_nodes_from(layer_nodes)
                
                # Add edges based on weight strength
                weight_threshold = np.std(weights) * 0.5  # Significant connections only
                
                for i in range(rows):
                    for j in range(cols):
                        if abs(weights[i, j]) > weight_threshold:
                            graph.add_edge(
                                node_id + i, 
                                node_id + rows + j,
                                weight=abs(weights[i, j])
                            )
                
                node_id += rows + cols
        
        return graph
    
    def _calculate_clustering(self, graph: nx.Graph) -> float:
        """Calculate average clustering coefficient."""
        if graph.number_of_nodes() == 0:
            return 0.0
        
        try:
            return nx.average_clustering(graph)
        except:
            return 0.0
    
    def _calculate_path_length(self, graph: nx.Graph) -> float:
        """Calculate average shortest path length."""
        if graph.number_of_nodes() == 0:
            return 0.0
        
        try:
            if nx.is_connected(graph):
                return nx.average_shortest_path_length(graph)
            else:
                # Handle disconnected graph
                components = list(nx.connected_components(graph))
                lengths = []
                for component in components:
                    subgraph = graph.subgraph(component)
                    if len(component) > 1:
                        lengths.append(nx.average_shortest_path_length(subgraph))
                
                return np.mean(lengths) if lengths else 0.0
        except:
            return 0.0
    
    def _calculate_modularity(self, graph: nx.Graph) -> float:
        """Calculate network modularity."""
        if graph.number_of_nodes() == 0:
            return 0.0
        
        try:
            # Use Louvain community detection
            import networkx.algorithms.community as nx_comm
            communities = nx_comm.greedy_modularity_communities(graph)
            return nx_comm.modularity(graph, communities)
        except:
            return 0.0
    
    def _detect_consciousness_basins(self, weight_matrices: List[np.ndarray]) -> Dict[str, List[int]]:
        """
        Detect consciousness basins using hierarchical clustering.
        
        Args:
            weight_matrices: Layer weight matrices
            
        Returns:
            Dictionary mapping basin names to neuron indices
        """
        basins = {}
        basin_count = 0
        
        for layer_idx, weights in enumerate(weight_matrices):
            if len(weights.shape) != 2:
                continue
            
            # Calculate neuron similarity matrix
            similarities = self._calculate_neuron_similarities(weights)
            
            # Hierarchical clustering to find basins
            if similarities.shape[0] > self.min_basin_size:
                try:
                    linkage_matrix = linkage(1 - similarities, method='ward')
                    clusters = fcluster(linkage_matrix, 
                                      1 - self.similarity_threshold, 
                                      criterion='distance')
                    
                    # Group neurons by cluster
                    unique_clusters = np.unique(clusters)
                    for cluster_id in unique_clusters:
                        cluster_neurons = np.where(clusters == cluster_id)[0].tolist()
                        
                        if len(cluster_neurons) >= self.min_basin_size:
                            basin_name = f"layer_{layer_idx}_basin_{basin_count}"
                            basins[basin_name] = cluster_neurons
                            basin_count += 1
                
                except Exception as e:
                    warnings.warn(f"Basin detection failed for layer {layer_idx}: {e}")
                    continue
        
        return basins
    
    def _calculate_neuron_similarities(self, weights: np.ndarray) -> np.ndarray:
        """
        Calculate pairwise neuron similarities.
        
        Args:
            weights: Layer weight matrix
            
        Returns:
            Similarity matrix
        """
        # Use correlation as similarity metric
        correlations = np.corrcoef(weights)
        
        # Handle NaN values (replace with 0)
        correlations = np.nan_to_num(correlations, nan=0.0)
        
        # Convert to similarity (absolute correlation)
        similarities = np.abs(correlations)
        
        return similarities
    
    def _analyze_sub_pathways(self, weight_matrices: List[np.ndarray]) -> float:
        """
        Analyze sub-pathway density (word-type separation).
        
        Args:
            weight_matrices: Layer weight matrices
            
        Returns:
            Sub-pathway density score
        """
        total_density = 0.0
        layer_count = 0
        
        for weights in weight_matrices:
            if len(weights.shape) != 2:
                continue
            
            # Calculate local clustering within weight matrix
            # Higher clustering = better sub-pathway formation
            try:
                # Build local adjacency matrix
                threshold = np.std(weights) * 0.3
                adj_matrix = (np.abs(weights) > threshold).astype(int)
                
                # Calculate local clustering coefficient
                local_graph = nx.from_numpy_array(adj_matrix)
                if local_graph.number_of_nodes() > 0:
                    local_clustering = nx.average_clustering(local_graph)
                    total_density += local_clustering
                    layer_count += 1
            
            except Exception:
                continue
        
        return total_density / max(layer_count, 1)
    
    def _calculate_small_world_coefficient(self, graph: nx.Graph) -> float:
        """Calculate small-world coefficient."""
        if graph.number_of_nodes() == 0:
            return 0.0
        
        try:
            clustering = self._calculate_clustering(graph)
            path_length = self._calculate_path_length(graph)
            
            # Compare to random graph
            num_nodes = graph.number_of_nodes()
            num_edges = graph.number_of_edges()
            
            if num_nodes > 0 and num_edges > 0:
                # Expected values for random graph
                random_clustering = (2 * num_edges) / (num_nodes * (num_nodes - 1))
                random_path_length = np.log(num_nodes) / np.log(2 * num_edges / num_nodes)
                
                if random_clustering > 0 and random_path_length > 0:
                    # Small-world coefficient: high clustering, short path length
                    small_world = (clustering / random_clustering) / (path_length / random_path_length)
                    return min(small_world, 10.0)  # Cap at reasonable value
            
            return 0.0
        
        except:
            return 0.0
    
    def _calculate_consciousness_score(self, 
                                     clustering: float,
                                     path_length: float, 
                                     modularity: float,
                                     basin_count: int,
                                     sub_pathway_density: float,
                                     small_world: float) -> float:
        """
        Calculate overall consciousness topology score.
        
        Combines multiple topological metrics into single consciousness measure.
        """
        # Normalize metrics to 0-1 range
        norm_clustering = min(clustering, 1.0)
        norm_path_length = 1.0 / (1.0 + path_length)  # Shorter paths = better
        norm_modularity = max(0.0, min(modularity, 1.0))
        norm_basins = min(basin_count / 20.0, 1.0)  # Optimal ~20 basins
        norm_sub_pathways = min(sub_pathway_density, 1.0)
        norm_small_world = min(small_world / 5.0, 1.0)  # Small-world ~5
        
        # Weighted combination emphasizing consciousness-relevant metrics
        weights = {
            'clustering': 0.2,      # Local organization
            'path_length': 0.15,    # Global connectivity
            'modularity': 0.2,      # Functional separation
            'basins': 0.25,         # Consciousness basins (key!)
            'sub_pathways': 0.15,   # Word-type separation
            'small_world': 0.05     # Overall efficiency
        }
        
        consciousness_score = (
            weights['clustering'] * norm_clustering +
            weights['path_length'] * norm_path_length +
            weights['modularity'] * norm_modularity +
            weights['basins'] * norm_basins +
            weights['sub_pathways'] * norm_sub_pathways +
            weights['small_world'] * norm_small_world
        )
        
        return consciousness_score
    
    def _empty_metrics(self) -> TopologyMetrics:
        """Return empty metrics for models with no analyzable weights."""
        return TopologyMetrics(
            clustering_coefficient=0.0,
            path_length=0.0,
            modularity=0.0,
            basin_count=0,
            sub_pathway_density=0.0,
            small_world_coefficient=0.0,
            consciousness_topology_score=0.0,
            basin_separation={}
        )