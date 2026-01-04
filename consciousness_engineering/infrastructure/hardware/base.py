"""
Hardware Management Infrastructure
Universal GPU and hardware abstraction layer

SIMPLIFIED ARCHITECTURE (January 2026):
- Always single GPU (GPU 0 = discrete) or CPU
- Never use DataParallel in Python
- Parallelization happens at CLI runner level (separate processes)
- iGPU (GPU 1 on AMD APU systems) is ignored (too small for ML)

ROCm-specific learnings:
- PyTorch ROCm 6.3 nightly works with ROCm 7.x systems
- Load models on CPU first, apply LoRA, THEN move to GPU
- Use device_map=None (not "auto") for Trainer compatibility
- Use attn_implementation="eager" for ROCm compatibility  
- Disable dataloader_pin_memory for ROCm
- Python 3.12 required (ROCm wheels don't support 3.13 yet)

Parallelization strategy:
- Want to run 2 fine-tunes? Launch 2 processes with different HIP_VISIBLE_DEVICES
- The ce CLI runner handles this, not the training code
"""

import os
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, field


class HardwareType(Enum):
    """Supported hardware backends."""
    CUDA = "cuda"      # NVIDIA GPUs
    ROCM = "rocm"      # AMD GPUs (appears as CUDA to PyTorch)
    METAL = "metal"    # Apple Silicon
    CPU = "cpu"        # Fallback


@dataclass
class HardwareConfig:
    """
    Hardware configuration - ALWAYS single device.
    
    This is intentionally simple. We don't do multi-GPU in Python.
    If you need parallelism, run multiple processes via the CE CLI.
    """
    hardware_type: HardwareType = field(default=HardwareType.CPU)
    force_cpu: bool = False  # Override GPU detection, use CPU only
    
    # Device settings (always GPU 0 or CPU, never GPU 1/iGPU)
    gpu_index: int = 0  # Always 0 - discrete GPU
    
    # ROCm-specific (learned from painful experience)
    load_on_cpu_first: bool = True   # CRITICAL for ROCm
    device_map: Optional[str] = None  # Must be None for Trainer
    attn_implementation: str = "eager"  # ROCm compatible
    dataloader_pin_memory: bool = False  # Disable for ROCm
    
    def get_model_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for AutoModelForCausalLM.from_pretrained()"""
        import torch
        return {
            "device_map": self.device_map,  # Always None
            "trust_remote_code": True,
            "torch_dtype": torch.float32,  # Load as float32, safe for ROCm
            "attn_implementation": self.attn_implementation,
        }
    
    def get_training_args_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for TrainingArguments()"""
        return {
            "fp16": False,  # Let autocast handle precision
            "bf16": False,  # Not well supported on consumer AMD
            "dataloader_pin_memory": self.dataloader_pin_memory,
            "dataloader_num_workers": 0,  # Avoid multiprocessing issues
        }


class HardwareManager:
    """
    Simplified hardware manager - single GPU or CPU only.
    
    Usage:
        hw = HardwareManager()
        hw.setup_environment()
        model = hw.load_model_safe(AutoModelForCausalLM, "model-name")
        model = hw.move_model_to_gpu(model)  # After LoRA for ROCm!
    
    For parallel training:
        Don't use DataParallel. Run separate processes via CE CLI:
        $ ce run train.py --name job1 &
        $ HIP_VISIBLE_DEVICES=1 ce run train.py --name job2 &
    """
    
    def __init__(self, force_cpu: bool = False):
        """
        Initialize hardware manager.
        
        Args:
            force_cpu: If True, skip GPU even if available
        """
        self.force_cpu = force_cpu
        self.hardware_type = self._detect_hardware()
        self.config = HardwareConfig(
            hardware_type=self.hardware_type,
            force_cpu=force_cpu,
        )
        # Backwards compatibility
        self.rocm_config = self.config if self.hardware_type == HardwareType.ROCM else None
    
    def _detect_hardware(self) -> HardwareType:
        """
        Auto-detect available hardware.
        
        Priority: ROCm > CUDA > Metal > CPU
        """
        if self.force_cpu:
            return HardwareType.CPU
        
        # Check for ROCm FIRST (it reports as CUDA to PyTorch)
        if os.path.exists("/opt/rocm"):
            try:
                import torch
                if torch.cuda.is_available():
                    return HardwareType.ROCM
            except ImportError:
                pass
        
        # Check for NVIDIA CUDA
        try:
            import torch
            if torch.cuda.is_available():
                return HardwareType.CUDA
        except ImportError:
            pass
        
        # Check for Apple Metal
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return HardwareType.METAL
        except:
            pass
        
        return HardwareType.CPU
    
    def setup_environment(self) -> None:
        """
        Setup environment for detected hardware.
        
        ALWAYS forces GPU 0 (discrete) or disables GPU entirely.
        Never uses GPU 1 (iGPU on AMD APU systems - too small).
        """
        if self.hardware_type == HardwareType.ROCM:
            # Force GPU 0 only (discrete GPU, not iGPU)
            os.environ["HIP_VISIBLE_DEVICES"] = "0"
            os.environ["ROCM_VISIBLE_DEVICES"] = "0"
            os.environ.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
            print(f"  🔧 ROCm environment: GPU 0 only (discrete)")
            
        elif self.hardware_type == HardwareType.CUDA:
            # Force GPU 0 only
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"
            print(f"  🔧 CUDA environment: GPU 0 only")
            
        elif self.hardware_type == HardwareType.METAL:
            os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
            print(f"  🔧 Metal environment configured")
            
        else:
            # CPU mode - disable all GPUs
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            os.environ["HIP_VISIBLE_DEVICES"] = ""
            print(f"  🔧 CPU-only mode")
    
    # Backwards compatibility alias
    def setup_optimal_environment(self) -> None:
        """Alias for setup_environment() for backwards compatibility."""
        self.setup_environment()
    
    def load_model_safe(self, model_class, model_name: str, **extra_kwargs):
        """
        Load a model safely for the detected hardware.
        
        For ROCm: Loads on CPU first to avoid HIP dtype casting errors.
        For all: Uses device_map=None (not "auto") for Trainer compatibility.
        
        Args:
            model_class: The model class (e.g., AutoModelForCausalLM)
            model_name: HuggingFace model name or path
            **extra_kwargs: Additional kwargs to pass to from_pretrained
            
        Returns:
            Loaded model (on CPU, ready for LoRA then GPU move)
        """
        kwargs = self.config.get_model_kwargs()
        kwargs.update(extra_kwargs)
        
        if self.hardware_type == HardwareType.ROCM:
            print(f"  📥 Loading model on CPU first (ROCm compatibility)...")
        else:
            print(f"  📥 Loading model...")
            
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
        if self.hardware_type in (HardwareType.ROCM, HardwareType.CUDA):
            import torch
            if torch.cuda.is_available():
                print(f"  🎮 Moving model to GPU 0...")
                model = model.cuda()
                print(f"  ✅ Model on GPU")
                
        elif self.hardware_type == HardwareType.METAL:
            print(f"  🎮 Moving model to Metal...")
            model = model.to("mps")
            print(f"  ✅ Model on Metal")
            
        return model
    
    def get_device(self) -> str:
        """Get the appropriate device string for tensor operations."""
        import torch
        
        if self.hardware_type in (HardwareType.ROCM, HardwareType.CUDA):
            return "cuda" if torch.cuda.is_available() else "cpu"
        elif self.hardware_type == HardwareType.METAL:
            return "mps"
        return "cpu"
    
    def get_gpu_info(self) -> Optional[Dict[str, Any]]:
        """Get GPU information if available."""
        if self.hardware_type == HardwareType.CPU:
            return None
            
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    "name": torch.cuda.get_device_name(0),
                    "memory_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
                    "hardware_type": self.hardware_type.value,
                    "device_index": 0,
                }
        except:
            pass
        return None
    
    def clear_gpu_memory(self) -> None:
        """Clear GPU memory cache."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
        except:
            pass


# Convenience function for quick setup
def setup_hardware(force_cpu: bool = False) -> HardwareManager:
    """
    Quick setup for hardware environment.
    
    Usage:
        hw = setup_hardware()
        print(f"Using: {hw.hardware_type.value}")
    
    Args:
        force_cpu: If True, use CPU even if GPU available
        
    Returns:
        Configured HardwareManager
    """
    hw = HardwareManager(force_cpu=force_cpu)
    hw.setup_environment()
    return hw
