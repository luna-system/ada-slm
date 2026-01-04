"""
Training Programs Base Classes
==============================

Abstract base classes for all types of training programs in the consciousness 
engineering framework. Provides common interface and ROCm-safe infrastructure.
"""

import abc
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field

from ..infrastructure.hardware import HardwareManager
from ..infrastructure.monitoring import TrainingMonitor


@dataclass
class TrainingResult:
    """Result from any training operation."""
    program_name: str
    success: bool
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    model_path: Optional[str] = None
    final_loss: Optional[float] = None
    consciousness_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    
    @property
    def training_time(self) -> Optional[float]:
        """Training duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property 
    def training_time_hours(self) -> Optional[float]:
        """Training duration in hours."""
        time_sec = self.training_time
        return time_sec / 3600 if time_sec else None


@dataclass
class TrainingConfig:
    """Base configuration for training programs."""
    name: str
    description: str
    output_dir: str
    model_config: Dict[str, Any] = field(default_factory=dict)
    training_params: Dict[str, Any] = field(default_factory=dict)
    lora_config: Dict[str, Any] = field(default_factory=dict)
    gpu_config: Dict[str, Any] = field(default_factory=dict)
    monitoring_config: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default configurations."""
        # Set default GPU config if not provided
        if not self.gpu_config:
            self.gpu_config = {
                "device_index": 0,
                "clear_memory": True
            }
        
        # Set default monitoring config if not provided
        if not self.monitoring_config:
            self.monitoring_config = {
                "log_eigenvalues": True,
                "save_checkpoints": True,
                "eval_frequency": 200
            }


class TrainingProgram(abc.ABC):
    """
    Abstract base class for all training programs.
    
    Provides:
    - ROCm-safe GPU management
    - Training monitoring and logging
    - Result persistence  
    - Error handling and recovery
    - Common interface for all training types
    """
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Core infrastructure
        self.hardware_manager: Optional[HardwareManager] = None
        self.monitor: Optional[TrainingMonitor] = None
        self.results: List[TrainingResult] = []
        
    def setup_infrastructure(self) -> bool:
        """Setup GPU and monitoring infrastructure."""
        try:
            # Hardware setup - use consciousness_engineering infrastructure
            self.hardware_manager = HardwareManager()
            gpu_config = self.config.gpu_config
            
            # Setup optimal environment for detected hardware
            self.hardware_manager.setup_optimal_environment()
            
            # GPU memory isolation if requested
            if gpu_config.get('clear_memory', True):
                self.hardware_manager.isolate_gpu_memory()
            
            # Monitor setup
            self.monitor = TrainingMonitor(
                output_dir=self.output_dir,
                **self.config.monitoring_config
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Infrastructure setup failed: {e}")
            return False
    
    def cleanup_infrastructure(self) -> None:
        """Cleanup GPU memory and monitoring."""
        if self.hardware_manager:
            self.hardware_manager.isolate_gpu_memory()
        
        if self.monitor:
            self.monitor.close()
    
    @abc.abstractmethod
    def execute_training(self) -> List[TrainingResult]:
        """Execute the specific training program."""
        pass
    
    def run(self) -> List[TrainingResult]:
        """
        Main execution method for training program.
        
        Returns:
            List of training results
        """
        print(f"🚀 Starting {self.config.name}")
        print(f"📊 Description: {self.config.description}")
        
        # Setup infrastructure
        if not self.setup_infrastructure():
            return []
        
        try:
            # Execute training
            results = self.execute_training()
            self.results.extend(results)
            
            # Save results
            self.save_results()
            
            return results
            
        except KeyboardInterrupt:
            print("⏹️  Training interrupted by user")
            return self.results
            
        except Exception as e:
            print(f"💥 Training failed: {e}")
            
            # Create failure result
            failure_result = TrainingResult(
                program_name=self.config.name,
                success=False,
                start_time=datetime.now(),
                end_time=datetime.now(),
                error_message=str(e)
            )
            self.results.append(failure_result)
            return self.results
            
        finally:
            self.cleanup_infrastructure()
    
    def save_results(self) -> None:
        """Save training results to JSON."""
        import json
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.output_dir / f"training_results_{timestamp}.json"
        
        # Convert results to serializable format
        results_data = {
            "program": self.config.name,
            "description": self.config.description, 
            "timestamp": timestamp,
            "config": {
                "model": self.config.model_config,
                "training": self.config.training_params,
                "lora": self.config.lora_config
            },
            "results": [
                {
                    "program_name": r.program_name,
                    "success": r.success,
                    "start_time": r.start_time.isoformat() if r.start_time else None,
                    "end_time": r.end_time.isoformat() if r.end_time else None,
                    "model_path": r.model_path,
                    "final_loss": r.final_loss,
                    "consciousness_score": r.consciousness_score,
                    "training_time_hours": r.training_time_hours,
                    "metadata": r.metadata,
                    "error_message": r.error_message
                }
                for r in self.results
            ],
            "summary": {
                "total_results": len(self.results),
                "successful_results": sum(1 for r in self.results if r.success),
                "total_training_time_hours": sum(r.training_time_hours or 0 for r in self.results)
            }
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"💾 Results saved: {results_file}")


class TrainingHarness:
    """
    Unified training harness that can execute any training program.
    
    This is the main entry point for all training operations in the 
    consciousness engineering framework.
    """
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_program(self, program: TrainingProgram) -> List[TrainingResult]:
        """Execute a training program using this harness."""
        return program.run()
    
    def create_config(
        self,
        name: str,
        description: str,
        program_type: str = "custom",
        **kwargs
    ) -> TrainingConfig:
        """Create a training configuration."""
        
        # Default configurations
        default_gpu_config = {
            "device_index": 0,
            "clear_memory": True
        }
        
        default_monitoring_config = {
            "log_eigenvalues": True,
            "save_checkpoints": True,
            "eval_frequency": 200
        }
        
        output_dir = self.output_dir / name
        
        return TrainingConfig(
            name=name,
            description=description,
            output_dir=str(output_dir),
            gpu_config={**default_gpu_config, **kwargs.get('gpu_config', {})},
            monitoring_config={**default_monitoring_config, **kwargs.get('monitoring_config', {})},
            **{k: v for k, v in kwargs.items() if k not in ['gpu_config', 'monitoring_config']}
        )