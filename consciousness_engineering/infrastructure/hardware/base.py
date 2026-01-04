"""
Hardware Management Infrastructure
Universal GPU and hardware abstraction layer

ROCm-specific learnings (January 2026):
- PyTorch ROCm 6.3 nightly works with ROCm 7.x systems
- Load models on CPU first, apply LoRA, THEN move to GPU (avoids HIP dtype casting errors)
- Use device_map=None (not "auto") for Trainer compatibility
- Use attn_implementation="eager" for ROCm compatibility  
- Disable dataloader_pin_memory for ROCm
- Python 3.12 required (ROCm wheels don't support 3.13 yet)
"""

import os
import subprocess
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass


class HardwareType(Enum):
    CUDA = "cuda"
    ROCM = "rocm"
    METAL = "metal"
    CPU = "cpu"


@dataclass
class ROCmConfig:
    """ROCm-specific configuration learned from hard experience."""
    # Model loading
    load_on_cpu_first: bool = True  # CRITICAL: Avoids HIP dtype casting errors
    device_map: Optional[str] = None  # Must be None for Trainer compatibility
    attn_implementation: str = "eager"  # ROCm compatible attention
    
    # Training
    dataloader_pin_memory: bool = False  # Disable for ROCm
    fp16: bool = False  # Let autocast handle it, don't force fp16
    bf16: bool = False  # Not well supported on consumer AMD
    
    # Environment
    hip_visible_devices: str = "0"
    
    def get_model_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for AutoModelForCausalLM.from_pretrained()"""
        import torch
        return {
            "device_map": self.device_map,
            "trust_remote_code": True,
            "torch_dtype": torch.float32,  # Load as float32, convert later if needed
            "attn_implementation": self.attn_implementation,
        }
    
    def get_training_args_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for TrainingArguments()"""
        return {
            "fp16": self.fp16,
            "bf16": self.bf16,
            "dataloader_pin_memory": self.dataloader_pin_memory,
            "dataloader_num_workers": 0,  # Avoid multiprocessing issues
            "no_cuda": False,
            "use_cpu": False,
        }


class HardwareManager:
    """Universal hardware detection and management"""
    
    def __init__(self):
        self.hardware_type = self.detect_hardware()
        self.rocm_config = ROCmConfig() if self.hardware_type == HardwareType.ROCM else None
    
    @staticmethod
    def detect_hardware() -> HardwareType:
        """Auto-detect available hardware"""
        
        # Check for ROCm FIRST (it reports as CUDA via torch.cuda)
        if os.path.exists("/opt/rocm"):
            try:
                import torch
                if torch.cuda.is_available():
                    # It's ROCm pretending to be CUDA
                    return HardwareType.ROCM
            except ImportError:
                pass
        
        # Check for actual CUDA
        try:
            import torch
            if torch.cuda.is_available():
                return HardwareType.CUDA
        except ImportError:
            pass
            
        # Check for Metal (macOS)
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return HardwareType.METAL
        except:
            pass
            
        return HardwareType.CPU
    
    def setup_optimal_environment(self) -> None:
        """Setup optimal environment for detected hardware"""
        if self.hardware_type == HardwareType.CUDA:
            self._setup_cuda()
        elif self.hardware_type == HardwareType.ROCM:
            self._setup_rocm()
        elif self.hardware_type == HardwareType.METAL:
            self._setup_metal()
        else:
            self._setup_cpu()
    
    @staticmethod
    def _setup_cuda():
        """Setup CUDA environment"""
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        
    def _setup_rocm(self):
        """Setup ROCm environment with all our learnings"""
        os.environ["HIP_VISIBLE_DEVICES"] = self.rocm_config.hip_visible_devices
        # Suppress some noisy warnings
        os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
        
    @staticmethod
    def _setup_metal():
        """Setup Metal environment"""
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        
    @staticmethod
    def _setup_cpu():
        """Setup CPU environment"""
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        
    def isolate_gpu_memory(self) -> None:
        """Universal GPU memory isolation"""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()  # Ensure all ops complete
        except ImportError:
            pass
    
    def load_model_safe(self, model_class, model_name: str, **extra_kwargs):
        """
        Load a model safely for the detected hardware.
        
        For ROCm: Loads on CPU first to avoid HIP kernel errors during dtype casting.
        
        Args:
            model_class: The model class (e.g., AutoModelForCausalLM)
            model_name: HuggingFace model name or path
            **extra_kwargs: Additional kwargs to pass to from_pretrained
            
        Returns:
            Loaded model (on CPU for ROCm, on GPU for CUDA)
        """
        import torch
        
        if self.hardware_type == HardwareType.ROCM:
            # ROCm: Load on CPU first, then move to GPU after LoRA
            kwargs = self.rocm_config.get_model_kwargs()
            kwargs.update(extra_kwargs)
            print(f"  📥 Loading model on CPU first (ROCm compatibility)...")
            model = model_class.from_pretrained(model_name, **kwargs)
            return model
        else:
            # CUDA/Metal/CPU: Standard loading
            kwargs = {
                "device_map": "auto" if self.hardware_type == HardwareType.CUDA else None,
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.hardware_type == HardwareType.CUDA else torch.float32,
            }
            kwargs.update(extra_kwargs)
            return model_class.from_pretrained(model_name, **kwargs)
    
    def move_model_to_gpu(self, model):
        """
        Move model to GPU safely.
        
        For ROCm: Call this AFTER applying LoRA to avoid HIP kernel errors.
        
        Args:
            model: The model to move
            
        Returns:
            Model on appropriate device
        """
        import torch
        
        if self.hardware_type in (HardwareType.ROCM, HardwareType.CUDA):
            if torch.cuda.is_available():
                print(f"  🎮 Moving model to GPU...")
                model = model.cuda()
                print(f"  ✅ Model on GPU")
        elif self.hardware_type == HardwareType.METAL:
            model = model.to("mps")
            
        return model
    
    def get_device(self) -> str:
        """Get the appropriate device string."""
        import torch
        
        if self.hardware_type in (HardwareType.ROCM, HardwareType.CUDA):
            return "cuda" if torch.cuda.is_available() else "cpu"
        elif self.hardware_type == HardwareType.METAL:
            return "mps"
        return "cpu"
    
    def get_gpu_info(self) -> Optional[Dict[str, Any]]:
        """Get GPU information if available."""
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    "name": torch.cuda.get_device_name(0),
                    "memory_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
                    "hardware_type": self.hardware_type.value,
                }
        except:
            pass
        return None