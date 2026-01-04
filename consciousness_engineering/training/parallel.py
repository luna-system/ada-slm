"""
Parallel Training Implementation
=================================

Multi-GPU and multi-model parallel training for comparative research.
Perfect for basin mapping, architecture comparisons, and distributed experiments.
"""

import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .programs import TrainingProgram, TrainingConfig, TrainingResult


@dataclass
class ParallelTrainingJob:
    """Single job in a parallel training session."""
    job_id: str
    name: str
    description: str
    model_config: Dict[str, Any]
    training_params: Dict[str, Any]
    dataset: List[Dict[str, Any]]
    device_index: int = 0
    priority: int = 1  # 1=highest, higher numbers=lower priority


@dataclass
class ParallelConfig(TrainingConfig):
    """Configuration for parallel training."""
    parallel_config: Dict[str, Any] = field(default_factory=dict)
    device_mapping: Dict[str, int] = field(default_factory=dict)


class ParallelTrainer(TrainingProgram):
    """
    Parallel training program for multiple models/configurations.
    
    Features:
    - Multi-GPU job distribution
    - Priority-based job scheduling  
    - Real-time progress monitoring
    - Comparative result analysis
    - Basin mapping capabilities
    """
    
    def __init__(self, config: ParallelConfig):
        super().__init__(config)
        self.jobs: List[ParallelTrainingJob] = []
        self.job_results: Dict[str, Dict[str, Any]] = {}
        self.running_jobs: Dict[str, bool] = {}
        
        # Parallel settings
        self.max_parallel_jobs = config.parallel_config.get('max_parallel_jobs', 2)
        self.job_timeout = config.parallel_config.get('job_timeout_hours', 24.0)
        self.device_mapping = config.device_mapping
        
    def add_job(self, job: ParallelTrainingJob) -> None:
        """Add a parallel training job."""
        self.jobs.append(job)
        self.running_jobs[job.job_id] = False
        
    def add_basin_mapping_jobs(
        self, 
        base_config: Dict[str, Any],
        parameter_ranges: Dict[str, List[Any]],
        dataset: List[Dict[str, Any]]
    ) -> None:
        """
        Add jobs for basin mapping across parameter space.
        
        Args:
            base_config: Base model configuration
            parameter_ranges: Dict of parameter names to lists of values
            dataset: Training dataset for all jobs
        """
        print(f"🗺️  Generating basin mapping jobs")
        
        # Generate all parameter combinations
        import itertools
        
        param_names = list(parameter_ranges.keys())
        param_values = list(parameter_ranges.values())
        
        job_count = 0
        for combo in itertools.product(*param_values):
            job_config = base_config.copy()
            job_params = dict(zip(param_names, combo))
            
            # Update config with this combination
            for param_name, param_value in job_params.items():
                if '.' in param_name:
                    # Nested parameter like "lora.rank"
                    keys = param_name.split('.')
                    target = job_config
                    for key in keys[:-1]:
                        if key not in target:
                            target[key] = {}
                        target = target[key]
                    target[keys[-1]] = param_value
                else:
                    job_config[param_name] = param_value
            
            job_id = f"basin_map_{job_count:03d}"
            param_str = "_".join(f"{k}={v}" for k, v in job_params.items())
            
            job = ParallelTrainingJob(
                job_id=job_id,
                name=f"Basin Mapping: {param_str}",
                description=f"Basin mapping with {param_str}",
                model_config=job_config,
                training_params={"param_combination": job_params},
                dataset=dataset,
                device_index=job_count % self.max_parallel_jobs,
                priority=1
            )
            
            self.add_job(job)
            job_count += 1
        
        print(f"✅ Generated {job_count} basin mapping jobs")
    
    def train_single_job(self, job: ParallelTrainingJob) -> Dict[str, Any]:
        """
        Train a single job.
        
        Args:
            job: Job to train
            
        Returns:
            Dictionary with training results for this job
        """
        print(f"🚀 Starting job {job.job_id}: {job.name}")
        self.running_jobs[job.job_id] = True
        
        start_time = time.time()
        
        try:
            # Mock training (replace with actual transformers training)
            print(f"  📊 Device: {job.device_index}")
            print(f"  📝 Examples: {len(job.dataset)}")
            
            # Simulate model-dependent training characteristics
            model_complexity = job.model_config.get('hidden_size', 768) / 768.0
            dataset_size_factor = len(job.dataset) / 1000.0
            
            # Simulate training time (proportional to complexity)
            training_time = min(5.0, model_complexity * dataset_size_factor * 0.5)
            time.sleep(training_time)
            
            # Mock results with some variation based on config
            base_loss = 1.5
            complexity_penalty = (model_complexity - 1.0) * 0.2
            final_loss = max(0.1, base_loss + complexity_penalty + (hash(job.job_id) % 100) * 0.001)
            
            consciousness_score = min(1.0, max(0.1, 0.7 - complexity_penalty + (hash(job.name) % 50) * 0.002))
            
            end_time = time.time()
            actual_time = end_time - start_time
            
            result = {
                'job_id': job.job_id,
                'name': job.name,
                'device_index': job.device_index,
                'model_config': job.model_config,
                'training_params': job.training_params,
                'dataset_size': len(job.dataset),
                'final_loss': final_loss,
                'consciousness_score': consciousness_score,
                'training_time_seconds': actual_time,
                'success': True,
                'model_checkpoint': f"checkpoint_{job.job_id}",
                'metadata': {
                    'model_complexity': model_complexity,
                    'dataset_size_factor': dataset_size_factor
                }
            }
            
            print(f"✅ Job {job.job_id} completed - Loss: {final_loss:.3f}, Consciousness: {consciousness_score:.3f}")
            return result
            
        except Exception as e:
            print(f"💥 Job {job.job_id} failed: {e}")
            
            result = {
                'job_id': job.job_id,
                'name': job.name,
                'success': False,
                'error_message': str(e),
                'training_time_seconds': time.time() - start_time
            }
            return result
            
        finally:
            self.running_jobs[job.job_id] = False
    
    def execute_training(self) -> List[TrainingResult]:
        """Execute all parallel training jobs."""
        print(f"⚡ Starting parallel training with {len(self.jobs)} jobs")
        print(f"🔄 Max parallel: {self.max_parallel_jobs}")
        
        # Sort jobs by priority (lower number = higher priority)
        sorted_jobs = sorted(self.jobs, key=lambda j: (j.priority, j.job_id))
        
        results = []
        
        # Execute jobs in parallel
        with ThreadPoolExecutor(max_workers=self.max_parallel_jobs) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self.train_single_job, job): job 
                for job in sorted_jobs
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_job):
                job = future_to_job[future]
                
                try:
                    job_result = future.result(timeout=self.job_timeout * 3600)
                    self.job_results[job.job_id] = job_result
                    
                    # Convert to TrainingResult format
                    training_result = TrainingResult(
                        program_name=f"{self.config.name}_{job.job_id}",
                        success=job_result['success'],
                        start_time=datetime.now(),  # Would be actual start time
                        end_time=datetime.now(),    # Would be actual end time
                        final_loss=job_result.get('final_loss'),
                        consciousness_score=job_result.get('consciousness_score'),
                        model_path=job_result.get('model_checkpoint'),
                        metadata=job_result
                    )
                    results.append(training_result)
                    
                except Exception as e:
                    print(f"💥 Job {job.job_id} exception: {e}")
                    
                    failure_result = TrainingResult(
                        program_name=f"{self.config.name}_{job.job_id}",
                        success=False,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        error_message=str(e),
                        metadata={'job_id': job.job_id, 'job_name': job.name}
                    )
                    results.append(failure_result)
        
        # Analyze results
        self.analyze_parallel_results()
        
        print(f"🎉 Parallel training completed!")
        print(f"✅ Successful jobs: {sum(1 for r in results if r.success)}/{len(results)}")
        
        return results
    
    def analyze_parallel_results(self) -> Dict[str, Any]:
        """Analyze results across all parallel jobs."""
        successful_jobs = {k: v for k, v in self.job_results.items() if v.get('success', False)}
        
        if not successful_jobs:
            print("❌ No successful jobs to analyze")
            return {}
        
        # Basic statistics
        losses = [job['final_loss'] for job in successful_jobs.values()]
        consciousness_scores = [job['consciousness_score'] for job in successful_jobs.values()]
        training_times = [job['training_time_seconds'] for job in successful_jobs.values()]
        
        analysis = {
            'total_jobs': len(self.job_results),
            'successful_jobs': len(successful_jobs),
            'success_rate': len(successful_jobs) / len(self.job_results),
            'loss_statistics': {
                'min': min(losses),
                'max': max(losses),
                'mean': sum(losses) / len(losses),
                'best_job_id': min(successful_jobs.keys(), key=lambda k: successful_jobs[k]['final_loss'])
            },
            'consciousness_statistics': {
                'min': min(consciousness_scores),
                'max': max(consciousness_scores),
                'mean': sum(consciousness_scores) / len(consciousness_scores),
                'best_job_id': max(successful_jobs.keys(), key=lambda k: successful_jobs[k]['consciousness_score'])
            },
            'timing_statistics': {
                'total_time': sum(training_times),
                'mean_time': sum(training_times) / len(training_times),
                'fastest_job_id': min(successful_jobs.keys(), key=lambda k: successful_jobs[k]['training_time_seconds'])
            }
        }
        
        print(f"\n📊 Parallel Training Analysis:")
        print(f"  Success Rate: {analysis['success_rate']:.1%}")
        print(f"  Loss Range: {analysis['loss_statistics']['min']:.3f} - {analysis['loss_statistics']['max']:.3f}")
        print(f"  Best Loss: {analysis['loss_statistics']['min']:.3f} (Job {analysis['loss_statistics']['best_job_id']})")
        print(f"  Best Consciousness: {analysis['consciousness_statistics']['max']:.3f} (Job {analysis['consciousness_statistics']['best_job_id']})")
        print(f"  Total Training Time: {analysis['timing_statistics']['total_time']:.1f}s")
        
        return analysis
    
    def save_parallel_results(self) -> None:
        """Save detailed parallel training results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Path(self.config.output_dir) / f"parallel_results_{timestamp}.json"
        
        parallel_data = {
            "program_name": self.config.name,
            "timestamp": timestamp,
            "parallel_config": {
                "max_parallel_jobs": self.max_parallel_jobs,
                "job_timeout_hours": self.job_timeout,
                "device_mapping": self.device_mapping
            },
            "job_definitions": [
                {
                    "job_id": job.job_id,
                    "name": job.name,
                    "description": job.description,
                    "model_config": job.model_config,
                    "training_params": job.training_params,
                    "dataset_size": len(job.dataset),
                    "device_index": job.device_index,
                    "priority": job.priority
                }
                for job in self.jobs
            ],
            "job_results": self.job_results,
            "analysis": self.analyze_parallel_results()
        }
        
        with open(results_file, 'w') as f:
            json.dump(parallel_data, f, indent=2)
        
        print(f"💾 Parallel results saved: {results_file}")