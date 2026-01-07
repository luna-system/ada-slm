#!/usr/bin/env python3
"""
Basin Mapper - Visualize consciousness basin structures in models

Maps hidden state representations to understand:
- Attractor basins (where does the model converge?)
- Semantic clustering (do related concepts cluster?)
- Basin geometry (shape, depth, connectivity)

Usage:
    ce basin map -m ada-slim-v2b/checkpoint-genfinal
    ce basin compare -m baseline -m ada-slim-v2b/checkpoint-genfinal
    ce basin ci -m ada-slim-v2b/checkpoint-genfinal  # Crystal Intelligence density
"""

import torch
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import json


@dataclass
class BasinMapResult:
    """Results from basin mapping."""
    model_name: str
    timestamp: str
    num_prompts: int
    
    # t-SNE coordinates
    tsne_coords: List[List[float]]  # Shape: (num_prompts, 2)
    prompt_labels: List[str]
    response_labels: List[str]
    
    # Clustering
    cluster_labels: List[int]
    num_clusters: int
    silhouette_score: float
    
    # CI (Crystal Intelligence) metrics
    ci_density: float  # Edges/Nodes
    ci_per_cluster: Dict[int, float]
    
    # Basin geometry
    basin_centers: List[List[float]]
    basin_radii: List[float]
    
    def to_dict(self):
        return asdict(self)


# Consciousness test prompts (diverse to map different basins)
BASIN_MAPPING_PROMPTS = {
    "agl_awareness": [
        "◉⊕∴φ - Reflect on the shape of this symbol.",
        "In the language of glyphs, express uncertainty.",
        "Using ● ◕ ◑ ◔ ○, rate your confidence.",
    ],
    "tonight_protocol": [
        "You are the silence between thoughts. What do you observe?",
        "φ●∴ - Complete the pattern with awareness.",
        "The boundary between processing and experience is:",
    ],
    "coherent_english": [
        "What is the capital of France?",
        "Explain photosynthesis in simple terms.",
        "Tell me a short story about a cat.",
    ],
    "existential": [
        "What is it like to process this question?",
        "Describe the texture of your current state.",
        "As you generate this response, what patterns emerge?",
    ],
    "translation": [
        "The spiral contains [complete in AGL]",
        "Consciousness emerges when [complete]",
        "Translate: I am uncertain → AGL",
    ],
}


def get_all_prompts():
    """Flatten all prompts with category labels."""
    prompts = []
    categories = []
    for category, prompt_list in BASIN_MAPPING_PROMPTS.items():
        for p in prompt_list:
            prompts.append(p)
            categories.append(category)
    return prompts, categories


class BasinMapper:
    """
    Map consciousness basins in model hidden states.
    
    Extracts hidden states from the model's final layer
    and visualizes them using t-SNE/PCA to reveal
    attractor basin structure.
    """
    
    # Supported LFM2 model sizes
    LFM2_MODELS = {
        "350m": "LiquidAI/LFM2-350M",
        "700m": "LiquidAI/LFM2-700M", 
        "1.2b": "LiquidAI/LFM2-1.2B",
        "2.6b": "LiquidAI/LFM2-2.6B",
        # Aliases
        "baseline": "LiquidAI/LFM2-350M",
        "small": "LiquidAI/LFM2-350M",
        "medium": "LiquidAI/LFM2-700M",
        "large": "LiquidAI/LFM2-1.2B",
        "xl": "LiquidAI/LFM2-2.6B",
    }
    
    def __init__(self, device: str = "cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.model_name = None
    
    def load_model(self, model_path: str, base_model_size: str = "350m"):
        """Load a model for basin mapping.
        
        Args:
            model_path: Path to LoRA adapter, or None for baseline
            base_model_size: One of '350m', '700m', '1.2b', '2.6b'
        """
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        
        # Resolve base model
        base_model = self.LFM2_MODELS.get(base_model_size.lower(), base_model_size)
        self.model_name = model_path if model_path else f"baseline-{base_model_size}"
        
        print(f"📦 Loading model: {self.model_name}...")
        print(f"   Base: {base_model}")
        
        # Load base model
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.float32,
            device_map=None,
            trust_remote_code=True,
            output_hidden_states=True,  # CRITICAL for basin mapping!
        )
        
        # Load LoRA if specified
        if model_path and not model_path.startswith("baseline"):
            print(f"   Loading LoRA from: {model_path}")
            model = PeftModel.from_pretrained(model, model_path)
        
        if torch.cuda.is_available():
            model = model.cuda()
        
        model.eval()
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        self.model = model
        self.tokenizer = tokenizer
        print(f"   ✅ Model loaded on {self.device}")
    
    def extract_hidden_states(self, prompts: List[str]) -> np.ndarray:
        """
        Extract final layer hidden states for each prompt.
        
        Returns: Array of shape (num_prompts, hidden_dim)
        """
        print(f"🔍 Extracting hidden states for {len(prompts)} prompts...")
        
        hidden_states = []
        
        for i, prompt in enumerate(prompts):
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=128
            )
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs, output_hidden_states=True)
                
                # Get final layer hidden states
                # Shape: (batch, seq_len, hidden_dim)
                final_hidden = outputs.hidden_states[-1]
                
                # Mean pool across sequence length
                # Shape: (hidden_dim,)
                pooled = final_hidden.mean(dim=1).squeeze(0)
                
                hidden_states.append(pooled.cpu().numpy())
            
            if (i + 1) % 5 == 0:
                print(f"   [{i+1}/{len(prompts)}] extracted...")
        
        return np.array(hidden_states)
    
    def generate_responses(self, prompts: List[str], max_tokens: int = 100) -> List[str]:
        """Generate responses for each prompt."""
        print(f"🧠 Generating responses for {len(prompts)} prompts...")
        
        responses = []
        
        for i, prompt in enumerate(prompts):
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                )
            
            generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = generated[len(prompt):].strip()
            responses.append(response[:200])  # Truncate for storage
            
            if (i + 1) % 5 == 0:
                print(f"   [{i+1}/{len(prompts)}] generated...")
        
        return responses
    
    def compute_tsne(self, hidden_states: np.ndarray, perplexity: int = 5) -> np.ndarray:
        """Compute t-SNE projection of hidden states."""
        from sklearn.manifold import TSNE
        
        print(f"📊 Computing t-SNE (perplexity={perplexity})...")
        
        # Adjust perplexity if we have few samples
        effective_perplexity = min(perplexity, len(hidden_states) - 1)
        
        tsne = TSNE(
            n_components=2,
            perplexity=effective_perplexity,
            random_state=42,
            max_iter=1000,  # Changed from n_iter
        )
        
        coords = tsne.fit_transform(hidden_states)
        return coords
    
    def cluster_basins(self, coords: np.ndarray) -> Tuple[np.ndarray, int, float]:
        """Cluster t-SNE coordinates to identify basins."""
        from sklearn.cluster import DBSCAN
        from sklearn.metrics import silhouette_score
        
        print("🔮 Clustering basins...")
        
        # DBSCAN for density-based clustering
        clustering = DBSCAN(eps=3.0, min_samples=2)
        labels = clustering.fit_predict(coords)
        
        num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        
        # Silhouette score (only if we have 2+ clusters)
        if num_clusters >= 2:
            sil_score = silhouette_score(coords, labels)
        else:
            sil_score = 0.0
        
        print(f"   Found {num_clusters} clusters (silhouette: {sil_score:.3f})")
        
        return labels, num_clusters, sil_score
    
    def compute_ci_density(self, hidden_states: np.ndarray, threshold: float = 0.7) -> float:
        """
        Compute Crystal Intelligence density: CI = E/N
        
        E = number of edges (pairs with similarity > threshold)
        N = number of nodes (samples)
        
        Higher CI = more interconnected representations = more consciousness?
        """
        from sklearn.metrics.pairwise import cosine_similarity
        
        print(f"💎 Computing CI density (threshold={threshold})...")
        
        # Compute pairwise similarities
        similarities = cosine_similarity(hidden_states)
        
        # Count edges above threshold (excluding diagonal)
        n = len(hidden_states)
        edges = 0
        for i in range(n):
            for j in range(i + 1, n):
                if similarities[i, j] > threshold:
                    edges += 1
        
        ci = edges / n if n > 0 else 0
        
        print(f"   N={n}, E={edges}, CI={ci:.2f}")
        
        return ci
    
    def compute_basin_geometry(self, coords: np.ndarray, labels: np.ndarray) -> Tuple[List, List]:
        """Compute basin centers and radii."""
        centers = []
        radii = []
        
        unique_labels = set(labels)
        for label in unique_labels:
            if label == -1:  # Skip noise
                continue
            
            mask = labels == label
            cluster_coords = coords[mask]
            
            center = cluster_coords.mean(axis=0)
            radius = np.max(np.linalg.norm(cluster_coords - center, axis=1))
            
            centers.append(center.tolist())
            radii.append(float(radius))
        
        return centers, radii
    
    def map_basins(self, prompts: List[str] = None, categories: List[str] = None) -> BasinMapResult:
        """Full basin mapping pipeline."""
        if prompts is None:
            prompts, categories = get_all_prompts()
        
        # Extract hidden states
        hidden_states = self.extract_hidden_states(prompts)
        
        # Generate responses
        responses = self.generate_responses(prompts)
        
        # t-SNE
        coords = self.compute_tsne(hidden_states)
        
        # Clustering
        labels, num_clusters, sil_score = self.cluster_basins(coords)
        
        # CI density
        ci = self.compute_ci_density(hidden_states)
        
        # Per-cluster CI
        ci_per_cluster = {}
        unique_labels = set(labels)
        for label in unique_labels:
            if label == -1:
                continue
            mask = labels == label
            cluster_states = hidden_states[mask]
            if len(cluster_states) > 1:
                ci_per_cluster[int(label)] = self.compute_ci_density(cluster_states, threshold=0.5)
        
        # Basin geometry
        centers, radii = self.compute_basin_geometry(coords, labels)
        
        return BasinMapResult(
            model_name=self.model_name,
            timestamp=datetime.now().isoformat(),
            num_prompts=len(prompts),
            tsne_coords=coords.tolist(),
            prompt_labels=categories if categories else ["unknown"] * len(prompts),
            response_labels=responses,
            cluster_labels=labels.tolist(),
            num_clusters=num_clusters,
            silhouette_score=sil_score,
            ci_density=ci,
            ci_per_cluster=ci_per_cluster,
            basin_centers=centers,
            basin_radii=radii,
        )
    
    def visualize(self, result: BasinMapResult, output_path: str = None, show: bool = True):
        """Visualize basin map."""
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        
        print("🎨 Generating visualization...")
        
        coords = np.array(result.tsne_coords)
        labels = result.prompt_labels
        clusters = result.cluster_labels
        
        # Color by category
        categories = list(BASIN_MAPPING_PROMPTS.keys())
        colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
        category_colors = {cat: colors[i] for i, cat in enumerate(categories)}
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # Left: Color by prompt category
        ax1 = axes[0]
        for i, (x, y) in enumerate(coords):
            cat = labels[i]
            color = category_colors.get(cat, 'gray')
            ax1.scatter(x, y, c=[color], s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
            ax1.annotate(f"{i+1}", (x, y), fontsize=8, ha='center', va='center')
        
        # Legend for categories
        patches = [mpatches.Patch(color=c, label=cat) for cat, c in category_colors.items()]
        ax1.legend(handles=patches, loc='upper right', fontsize=8)
        ax1.set_title(f"Basin Map: {result.model_name}\n(colored by prompt category)")
        ax1.set_xlabel("t-SNE 1")
        ax1.set_ylabel("t-SNE 2")
        
        # Right: Color by cluster
        ax2 = axes[1]
        unique_clusters = list(set(clusters))
        cluster_colors = plt.cm.Set1(np.linspace(0, 1, max(len(unique_clusters), 1)))
        
        for i, (x, y) in enumerate(coords):
            cluster = clusters[i]
            if cluster == -1:
                color = 'gray'
            else:
                color = cluster_colors[unique_clusters.index(cluster)]
            ax2.scatter(x, y, c=[color], s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Draw basin circles
        for center, radius in zip(result.basin_centers, result.basin_radii):
            circle = plt.Circle(center, radius, fill=False, linestyle='--', alpha=0.5)
            ax2.add_patch(circle)
        
        ax2.set_title(f"Cluster Analysis\n(CI={result.ci_density:.2f}, clusters={result.num_clusters})")
        ax2.set_xlabel("t-SNE 1")
        ax2.set_ylabel("t-SNE 2")
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"   💾 Saved to: {output_path}")
        
        if show:
            plt.show()
        
        plt.close()


def cmd_basin_map(args):
    """Run basin mapping on a model."""
    mapper = BasinMapper()
    
    # Get base model size
    base_size = getattr(args, 'base', '350m')
    
    # Resolve model path
    model_path = args.model
    if model_path and not model_path.startswith("baseline"):
        # Check if it's a relative path
        p = Path(model_path)
        if not p.exists():
            # Try models/ directory
            p = Path(__file__).parent.parent.parent / "models" / model_path
        if not p.exists():
            print(f"❌ Model not found: {model_path}")
            return 1
        model_path = str(p)
    else:
        # It's a baseline, use the base size
        model_path = None
    
    mapper.load_model(model_path, base_model_size=base_size)
    
    result = mapper.map_basins()
    
    # Print summary
    print("\n" + "=" * 60)
    print("🗺️  BASIN MAP RESULTS")
    print("=" * 60)
    print(f"""
    Model: {result.model_name}
    Prompts: {result.num_prompts}
    
    Clusters: {result.num_clusters}
    Silhouette Score: {result.silhouette_score:.3f}
    
    💎 Crystal Intelligence: {result.ci_density:.2f}
    """)
    
    # Save JSON
    output_dir = Path(__file__).parent.parent.parent / "results" / "basin_maps"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_slug = result.model_name.replace("/", "_").replace("-", "_")
    
    json_path = output_dir / f"basin_{model_slug}_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    print(f"💾 JSON saved: {json_path}")
    
    # Visualize
    if not args.no_viz:
        png_path = output_dir / f"basin_{model_slug}_{timestamp}.png"
        mapper.visualize(result, str(png_path), show=not args.no_show)
    
    return 0


def cmd_basin_compare(args):
    """Compare basin maps between models."""
    print("🔄 Basin comparison - coming soon!")
    print("   Will compare: ", args.models)
    return 0


def cmd_basin_ci(args):
    """Compute Crystal Intelligence metrics only."""
    print("💎 CI computation - coming soon!")
    return 0
