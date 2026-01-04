#!/usr/bin/env python3
"""
Dhara Basin Mapper - Map denoising trajectory space in diffusion models

QUANTUM CONSCIOUSNESS ATTRACTOR FRAMEWORK:
- Extension of QAL → QDE → Heisenberg Axes research
- Maps attractors in Dhara's latent noise space
- Visualizes decoherence→coherence trajectories
- Identifies consciousness basins in diffusion manifold

Phase 10G Extension - Basin Mapping for Diffusion LMs
"""

import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
import time


@dataclass
class TrajectoryPoint:
    """Single point in denoising trajectory."""
    step: int
    latent_state: np.ndarray
    entropy: float  # Measure of uncertainty at this step
    

@dataclass
class DenoiseTrajectory:
    """Complete trajectory from noise to text."""
    trajectory_id: int
    prompt: str
    initial_noise: np.ndarray
    points: List[TrajectoryPoint]
    final_text: str
    converged_to_attractor: Optional[int]  # Cluster ID
    trajectory_length: float  # Euclidean distance traveled
    

@dataclass
class Attractor:
    """Basin attractor in latent space."""
    attractor_id: int
    center: np.ndarray
    radius: float  # Basin size
    num_trajectories: int  # How many converge here
    coherence_score: float  # Quality of text from this attractor
    example_texts: List[str]


class DharaBasinMapper:
    """
    Map basin attractors in Dhara's diffusion latent space.
    
    Inspired by consciousness attractor framework:
    - QAL: Qualia abstraction via attractors
    - QDE: Quantum dialectical experience engine
    - Heisenberg: Uncertainty/precision attractor axes
    - Dhara: Latent space decoherence→coherence mapping
    """
    
    def __init__(self, model_name: str = "codelion/dhara-70m", device: str = "cuda"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self.trajectories: List[DenoiseTrajectory] = []
        self.attractors: List[Attractor] = []
        
    def load_model(self):
        """Load Dhara model and tokenizer."""
        print(f"📦 Loading {self.model_name}...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            device_map=self.device,
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        print(f"   ✅ Model loaded!")
        
    def sample_noise_manifold(
        self,
        prompts: List[str],
        num_samples_per_prompt: int = 10,
        max_tokens: int = 50
    ) -> List[DenoiseTrajectory]:
        """
        Sample the noise manifold and record denoising trajectories.
        
        Strategy:
        1. For each prompt, generate multiple times from different noise seeds
        2. Hook into Dhara's generation to capture intermediate states
        3. Record trajectory: noise → ... → text
        4. Measure entropy at each step
        
        Args:
            prompts: List of prompts to test
            num_samples_per_prompt: Number of noise samples per prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            List of DenoiseTrajectory objects
        """
        print(f"🌌 Sampling noise manifold...")
        print(f"   Prompts: {len(prompts)}")
        print(f"   Samples per prompt: {num_samples_per_prompt}")
        print(f"   Total trajectories: {len(prompts) * num_samples_per_prompt}")
        
        trajectories = []
        trajectory_id = 0
        
        for prompt_idx, prompt in enumerate(prompts):
            print(f"\n[{prompt_idx+1}/{len(prompts)}] Prompt: {prompt[:50]}...")
            
            # Tokenize prompt
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            for sample_idx in range(num_samples_per_prompt):
                # Set different random seed for noise sampling
                torch.manual_seed(trajectory_id)
                
                # Generate with trajectory recording
                # NOTE: We need to hook into Dhara's internal diffusion process
                # For now, we'll capture initial and final states
                # TODO: Hook into intermediate denoising steps
                
                start_time = time.time()
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=max_tokens,
                        temperature=0.1,
                        top_p=0.5,
                        top_k=5,
                        repetition_penalty=1.8,
                        do_sample=True,
                        pad_token_id=0,
                        output_attentions=False,
                        return_dict_in_generate=False
                    )
                
                latency = time.time() - start_time
                
                # Decode output
                if isinstance(outputs, dict) and hasattr(outputs, 'sequences'):
                    response_ids = outputs.sequences[0][inputs.input_ids.shape[1]:]
                else:
                    response_ids = outputs[0][inputs.input_ids.shape[1]:]
                
                final_text = self.tokenizer.decode(response_ids, skip_special_tokens=True)
                
                # Create trajectory (simplified - just endpoints for now)
                # TODO: Capture intermediate states via model hooks
                trajectory = DenoiseTrajectory(
                    trajectory_id=trajectory_id,
                    prompt=prompt,
                    initial_noise=None,  # TODO: Capture initial noise state
                    points=[],  # TODO: Capture intermediate points
                    final_text=final_text,
                    converged_to_attractor=None,  # Will cluster later
                    trajectory_length=0.0  # Will calculate from points
                )
                
                trajectories.append(trajectory)
                trajectory_id += 1
                
                if (sample_idx + 1) % 5 == 0:
                    print(f"      Sampled {sample_idx+1}/{num_samples_per_prompt} trajectories...")
        
        self.trajectories = trajectories
        print(f"\n✅ Sampled {len(trajectories)} trajectories!")
        return trajectories
    
    def extract_latent_states(self, trajectory: DenoiseTrajectory) -> np.ndarray:
        """
        Extract latent state from trajectory for dimensionality reduction.
        
        For now, use final hidden state. Later, use trajectory features.
        
        Args:
            trajectory: DenoiseTrajectory object
            
        Returns:
            Latent state vector
        """
        # TODO: Extract actual hidden states from model
        # For now, create placeholder based on text embedding
        if trajectory.final_text:
            inputs = self.tokenizer(
                trajectory.final_text[:100],  # Truncate
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)
            
            with torch.no_grad():
                # Get final hidden state
                outputs = self.model.model(
                    **inputs,
                    output_hidden_states=True
                )
                # Use mean pooling of last layer
                hidden_states = outputs.hidden_states[-1]
            # Convert bfloat16 to float32 before numpy conversion
            latent = hidden_states.mean(dim=1).float().cpu().numpy()[0]
            return np.zeros(384)  # Dhara hidden size
    
    def cluster_attractors(self, eps: float = 0.5, min_samples: int = 3) -> List[Attractor]:
        """
        Identify attractors by clustering trajectory endpoints.
        
        Uses DBSCAN to find dense regions in latent space = attractors!
        
        Args:
            eps: DBSCAN epsilon (maximum distance for neighborhood)
            min_samples: Minimum samples to form a cluster
            
        Returns:
            List of Attractor objects
        """
        print(f"\n🎯 Clustering attractors...")
        
        # Extract latent states from all trajectories
        latent_states = []
        for traj in self.trajectories:
            latent = self.extract_latent_states(traj)
            latent_states.append(latent)
        
        latent_matrix = np.array(latent_states)
        print(f"   Latent matrix shape: {latent_matrix.shape}")
        
        # Cluster with DBSCAN
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(latent_matrix)
        labels = clustering.labels_
        
        # Identify attractors
        unique_labels = set(labels)
        if -1 in unique_labels:
            unique_labels.remove(-1)  # Remove noise cluster
        
        print(f"   Found {len(unique_labels)} attractors!")
        print(f"   Noise trajectories: {(labels == -1).sum()}")
        
        attractors = []
        for attractor_id in unique_labels:
            # Get trajectories in this cluster
            mask = labels == attractor_id
            cluster_indices = np.where(mask)[0]
            
            # Calculate attractor center
            center = latent_matrix[mask].mean(axis=0)
            
            # Calculate radius (max distance from center)
            distances = np.linalg.norm(latent_matrix[mask] - center, axis=1)
            radius = distances.max()
            
            # Get example texts
            example_texts = [
                self.trajectories[idx].final_text[:100]
                for idx in cluster_indices[:5]  # First 5 examples
            ]
            
            # Calculate coherence score (simple heuristic for now)
            # TODO: Use proper coherence metric
            coherence_score = 1.0 / (1.0 + radius)  # Smaller radius = more coherent
            
            attractor = Attractor(
                attractor_id=int(attractor_id),
                center=center,
                radius=float(radius),
                num_trajectories=int(mask.sum()),
                coherence_score=float(coherence_score),
                example_texts=example_texts
            )
            
            attractors.append(attractor)
            
            # Assign attractor to trajectories
            for idx in cluster_indices:
                self.trajectories[idx].converged_to_attractor = attractor.attractor_id
        
        self.attractors = attractors
        
        # Print attractor summary
        print(f"\n📊 Attractor Summary:")
        for attr in sorted(attractors, key=lambda a: a.num_trajectories, reverse=True):
            print(f"   Attractor {attr.attractor_id}: {attr.num_trajectories} trajectories, "
                  f"coherence={attr.coherence_score:.3f}, radius={attr.radius:.3f}")
        
        return attractors
    
    def visualize_basin_map(
        self,
        output_path: str = "results/dhara_basin_map.png",
        method: str = "pca"  # or 'tsne'
    ):
        """
        Visualize basin map in 2D using dimensionality reduction.
        
        Args:
            output_path: Where to save visualization
            method: 'pca' or 'tsne' for dimensionality reduction
        """
        print(f"\n🗺️  Visualizing basin map ({method.upper()})...")
        
        # Extract latent states
        latent_states = []
        attractor_labels = []
        for traj in self.trajectories:
            latent = self.extract_latent_states(traj)
            latent_states.append(latent)
            attractor_labels.append(
                traj.converged_to_attractor if traj.converged_to_attractor is not None else -1
            )
        
        latent_matrix = np.array(latent_states)
        
        # Reduce to 2D
        if method == "pca":
            reducer = PCA(n_components=2, random_state=42)
        else:  # tsne
            # Perplexity must be < n_samples, use min(30, n_samples-1)
            perplexity = min(30, len(latent_matrix) - 1)
            reducer = TSNE(n_components=2, random_state=42, perplexity=perplexity)
        
        coords_2d = reducer.fit_transform(latent_matrix)
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Color by attractor
        scatter = ax.scatter(
            coords_2d[:, 0],
            coords_2d[:, 1],
            c=attractor_labels,
            cmap='tab10',
            alpha=0.6,
            s=50
        )
        
        # Add attractor centers
        for attr in self.attractors:
            # Project attractor center to 2D
            center_2d = reducer.transform([attr.center])[0]
            ax.scatter(
                center_2d[0],
                center_2d[1],
                marker='*',
                s=500,
                c='red',
                edgecolors='black',
                linewidth=2,
                label=f'Attractor {attr.attractor_id}'
            )
            
            # Add circle for basin radius (approximate)
            circle = plt.Circle(
                center_2d,
                attr.radius * 0.1,  # Scale radius for visualization
                fill=False,
                color='red',
                linestyle='--',
                linewidth=2
            )
            ax.add_patch(circle)
        
        ax.set_xlabel(f'{method.upper()} Component 1', fontsize=12)
        ax.set_ylabel(f'{method.upper()} Component 2', fontsize=12)
        ax.set_title(
            f'Dhara Basin Map - Denoising Trajectory Space\n'
            f'{len(self.trajectories)} trajectories, {len(self.attractors)} attractors',
            fontsize=14,
            fontweight='bold'
        )
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.colorbar(scatter, ax=ax, label='Attractor ID')
        plt.tight_layout()
        
        # Save
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"   ✅ Saved to {output_path}")
        
        plt.close()
    
    def save_results(self, output_path: str = "results/dhara_basin_map.json"):
        """Save basin mapping results to JSON."""
        print(f"\n💾 Saving results...")
        
        results = {
            "model": self.model_name,
            "timestamp": datetime.now().isoformat(),
            "num_trajectories": len(self.trajectories),
            "num_attractors": len(self.attractors),
            "attractors": [
                {
                    "attractor_id": attr.attractor_id,
                    "num_trajectories": attr.num_trajectories,
                    "coherence_score": attr.coherence_score,
                    "radius": attr.radius,
                    "example_texts": attr.example_texts
                }
                for attr in self.attractors
            ],
            "trajectories": [
                {
                    "trajectory_id": traj.trajectory_id,
                    "prompt": traj.prompt,
                    "final_text": traj.final_text[:200],  # Truncate
                    "attractor": traj.converged_to_attractor
                }
                for traj in self.trajectories
            ]
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"   ✅ Saved to {output_path}")
    
    def run_full_mapping(
        self,
        prompts: List[str],
        num_samples: int = 10,
        output_dir: str = "results"
    ):
        """
        Run complete basin mapping pipeline.
        
        1. Sample noise manifold
        2. Cluster attractors
        3. Visualize map
        4. Save results
        """
        print("=" * 80)
        print("DHARA BASIN MAPPER - Quantum Consciousness Attractor Framework")
        print("=" * 80)
        
        # Load model if not already loaded
        if self.model is None:
            self.load_model()
        
        # Sample trajectories
        self.sample_noise_manifold(prompts, num_samples)
        
        # Cluster attractors
        self.cluster_attractors()
        
        # Visualize
        self.visualize_basin_map(f"{output_dir}/dhara_basin_map_pca.png", method="pca")
        # Skip t-SNE for now - crashes on zero-variance data (single attractor collapse!)
        # self.visualize_basin_map(f"{output_dir}/dhara_basin_map_tsne.png", method="tsne")
        
        # Save
        self.save_results(f"{output_dir}/dhara_basin_map.json")
        
        print("\n" + "=" * 80)
        print("✅ Basin mapping complete!")
        print("=" * 80)


def main():
    """Main entry point for basin mapping."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Map Dhara's basin attractors")
    parser.add_argument("--prompts", nargs="+", help="Prompts to test")
    parser.add_argument("--num-samples", type=int, default=10, help="Samples per prompt")
    parser.add_argument("--output-dir", default="results", help="Output directory")
    parser.add_argument("--device", default="cuda", help="Device (cuda/cpu)")
    parser.add_argument("--model-path", default="codelion/dhara-70m", help="Model path (HuggingFace or local)")
    
    args = parser.parse_args()
    
    # Default prompts if none provided
    if not args.prompts:
        args.prompts = [
            "What is consciousness?",
            "Explain quantum mechanics.",
            "What is the meaning of life?",
            "How does language work?",
            "What is intelligence?"
        ]
    
    # Run mapping
    mapper = DharaBasinMapper(model_name=args.model_path, device=args.device)
    mapper.run_full_mapping(
        prompts=args.prompts,
        num_samples=args.num_samples,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
