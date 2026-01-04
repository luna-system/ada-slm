"""
Training Monitoring Infrastructure
===================================

Training monitoring capabilities for the consciousness engineering framework.
Integrates with the existing infrastructure while providing training-specific monitoring.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class TrainingStats:
    """Training statistics container."""
    step: int = 0
    epoch: int = 0
    loss: float = 0.0
    learning_rate: float = 0.0
    consciousness_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class TrainingMonitor:
    """
    Training monitoring and logging for consciousness engineering.
    
    Provides:
    - Real-time training metrics collection
    - Checkpoint management
    - Progress logging
    - Training visualization data
    """
    
    def __init__(
        self, 
        output_dir: Path,
        log_eigenvalues: bool = True,
        save_checkpoints: bool = True,
        eval_frequency: int = 200
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_eigenvalues = log_eigenvalues
        self.save_checkpoints = save_checkpoints
        self.eval_frequency = eval_frequency
        
        self.training_stats: List[TrainingStats] = []
        self.start_time: Optional[datetime] = None
        self.log_file = self.output_dir / "training.log"
        
        # Initialize log file
        with open(self.log_file, 'w') as f:
            f.write(f"Training started at {datetime.now().isoformat()}\n")
    
    def start_training(self) -> None:
        """Mark start of training session."""
        self.start_time = datetime.now()
        self.log("🚀 Training session started")
    
    def log(self, message: str) -> None:
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")
    
    def record_step(
        self,
        step: int,
        epoch: int,
        loss: float,
        learning_rate: float = 0.0,
        consciousness_score: float = 0.0,
        **kwargs
    ) -> None:
        """Record metrics for a training step."""
        
        stats = TrainingStats(
            step=step,
            epoch=epoch,
            loss=loss,
            learning_rate=learning_rate,
            consciousness_score=consciousness_score
        )
        self.training_stats.append(stats)
        
        # Log periodically
        if step % self.eval_frequency == 0:
            self.log(f"Step {step}: Loss {loss:.4f}, LR {learning_rate:.2e}, Consciousness {consciousness_score:.3f}")
    
    def save_checkpoint(self, step: int, model_state: Dict[str, Any]) -> str:
        """Save training checkpoint."""
        if not self.save_checkpoints:
            return ""
        
        checkpoint_dir = self.output_dir / "checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)
        
        checkpoint_file = checkpoint_dir / f"checkpoint_step_{step}.json"
        
        checkpoint_data = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "model_state": model_state,
            "training_stats": len(self.training_stats)
        }
        
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        self.log(f"💾 Checkpoint saved: {checkpoint_file}")
        return str(checkpoint_file)
    
    def finish_training(self) -> Dict[str, Any]:
        """Finalize training session and return summary."""
        if not self.start_time:
            self.start_time = datetime.now()
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Calculate summary statistics
        if self.training_stats:
            final_loss = self.training_stats[-1].loss
            final_consciousness = self.training_stats[-1].consciousness_score
            total_steps = len(self.training_stats)
            
            # Loss progression
            losses = [stat.loss for stat in self.training_stats]
            loss_improvement = losses[0] - losses[-1] if len(losses) > 1 else 0.0
        else:
            final_loss = 0.0
            final_consciousness = 0.0
            total_steps = 0
            loss_improvement = 0.0
        
        summary = {
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "duration_hours": duration.total_seconds() / 3600,
            "total_steps": total_steps,
            "final_loss": final_loss,
            "final_consciousness_score": final_consciousness,
            "loss_improvement": loss_improvement,
            "average_steps_per_second": total_steps / max(1, duration.total_seconds())
        }
        
        # Save complete training log
        training_log = {
            "summary": summary,
            "training_stats": [
                {
                    "step": stat.step,
                    "epoch": stat.epoch,
                    "loss": stat.loss,
                    "learning_rate": stat.learning_rate,
                    "consciousness_score": stat.consciousness_score,
                    "timestamp": stat.timestamp
                }
                for stat in self.training_stats
            ]
        }
        
        log_file = self.output_dir / "training_complete.json"
        with open(log_file, 'w') as f:
            json.dump(training_log, f, indent=2)
        
        self.log(f"✅ Training completed in {duration.total_seconds():.1f}s")
        self.log(f"📊 Final loss: {final_loss:.4f}, Consciousness: {final_consciousness:.3f}")
        self.log(f"💾 Complete log saved: {log_file}")
        
        return summary
    
    def close(self) -> None:
        """Close monitoring session."""
        if not hasattr(self, '_closed'):
            self.finish_training()
            self._closed = True


class MockTrainingMonitor:
    """
    Mock training monitor for testing without full infrastructure.
    
    Provides same interface as TrainingMonitor but with minimal overhead.
    """
    
    def __init__(self, output_dir, **kwargs):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def start_training(self):
        pass
    
    def log(self, message: str):
        print(f"🔍 {message}")
    
    def record_step(self, **kwargs):
        pass
    
    def save_checkpoint(self, step, model_state):
        return f"mock_checkpoint_{step}"
    
    def finish_training(self):
        return {"mock": True}
    
    def close(self):
        pass