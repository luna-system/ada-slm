#!/usr/bin/env bash
#
# ROCm PyTorch Environment Setup
# ==============================
# 
# This script sets up the VERY SPECIFIC environment needed for ROCm training.
# 
# WHY THIS EXISTS:
# - uv sync can't resolve pytorch-triton-rocm (doesn't exist in ROCm index)
# - pyproject.toml can't express "nightly torch from special index"
# - device_map="auto" breaks everything (we learned this the hard way)
# - Python 3.13 wheels don't exist for ROCm torch
#
# REQUIREMENTS:
# - Python 3.12.x exactly (not 3.13!)
# - ROCm 6.x or 7.x installed on system
# - uv package manager
#
# USAGE:
#   ./setup-rocm.sh         # Full setup
#   ./setup-rocm.sh verify  # Just verify existing setup
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# =============================================================================
# Verification Functions
# =============================================================================

verify_python_version() {
    info "Checking Python version..."
    
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+')
    if [[ "$PYTHON_VERSION" != "3.12" ]]; then
        error "Python 3.12.x required, found: $(python3 --version)\n   ROCm PyTorch wheels only exist for Python 3.12"
    fi
    success "Python 3.12 detected"
}

verify_rocm_installed() {
    info "Checking ROCm installation..."
    
    if [[ ! -d "/opt/rocm" ]]; then
        error "ROCm not found at /opt/rocm\n   Install ROCm first: https://rocm.docs.amd.com/"
    fi
    
    ROCM_VERSION=$(cat /opt/rocm/.info/version 2>/dev/null || echo "unknown")
    success "ROCm detected: $ROCM_VERSION"
}

verify_gpu() {
    info "Checking AMD GPU..."
    
    if ! command -v rocm-smi &> /dev/null; then
        warn "rocm-smi not found, skipping GPU check"
        return
    fi
    
    GPU_NAME=$(rocm-smi --showproductname 2>/dev/null | grep -oP 'Card series:\s*\K.*' | head -1 || echo "unknown")
    if [[ "$GPU_NAME" == "unknown" ]]; then
        warn "Could not detect GPU name"
    else
        success "GPU detected: $GPU_NAME"
    fi
}

verify_torch_rocm() {
    info "Checking PyTorch ROCm installation..."
    
    if [[ ! -d ".venv" ]]; then
        warn "No .venv found - run full setup first"
        return 1
    fi
    
    # Activate venv and check torch
    source .venv/bin/activate
    
    TORCH_VERSION=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "NOT INSTALLED")
    if [[ "$TORCH_VERSION" == "NOT INSTALLED" ]]; then
        error "PyTorch not installed in venv"
    fi
    
    if [[ "$TORCH_VERSION" != *"rocm"* ]]; then
        error "PyTorch installed but NOT ROCm build!\n   Found: $TORCH_VERSION\n   Expected: *+rocm*"
    fi
    success "PyTorch ROCm: $TORCH_VERSION"
    
    # Check CUDA availability (ROCm presents as CUDA to PyTorch)
    CUDA_AVAILABLE=$(python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null)
    if [[ "$CUDA_AVAILABLE" != "True" ]]; then
        error "torch.cuda.is_available() = False\n   ROCm driver issue?"
    fi
    success "torch.cuda.is_available() = True"
    
    # Check GPU name
    GPU_IN_TORCH=$(python -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')" 2>/dev/null)
    success "PyTorch sees GPU: $GPU_IN_TORCH"
    
    deactivate
}

# =============================================================================
# Setup Functions  
# =============================================================================

setup_venv() {
    info "Creating virtual environment with uv..."
    
    # Remove old venv if exists (clean slate)
    if [[ -d ".venv" ]]; then
        warn "Removing existing .venv for clean setup..."
        rm -rf .venv
    fi
    
    # Create venv with Python 3.12
    uv venv --python 3.12
    success "Virtual environment created"
}

install_dependencies() {
    info "Installing base dependencies (NOT torch yet)..."
    
    source .venv/bin/activate
    
    # Install everything EXCEPT torch first
    # This avoids uv trying to resolve torch from the wrong index
    uv pip install \
        transformers \
        datasets \
        peft \
        accelerate \
        safetensors \
        sentencepiece \
        protobuf \
        huggingface-hub \
        tqdm \
        numpy \
        scipy
    
    success "Base dependencies installed"
    deactivate
}

install_torch_rocm() {
    info "Installing PyTorch ROCm (nightly)..."
    
    source .venv/bin/activate
    
    # THE MAGIC COMMAND
    # This is the ONLY way to get ROCm torch that works:
    # - Nightly build (stable doesn't have all fixes)
    # - ROCm 6.3 wheels (works with ROCm 7.x runtime)
    # - Direct from PyTorch index (not PyPI)
    uv pip install torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/nightly/rocm6.3
    
    success "PyTorch ROCm installed"
    deactivate
}

# =============================================================================
# Main
# =============================================================================

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║         ROCm PyTorch Environment Setup for ada-slm          ║"
    echo "║                                                              ║"
    echo "║  Because uv sync doesn't understand our very specific needs ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check if just verifying
    if [[ "${1:-}" == "verify" ]]; then
        info "Verification mode - checking existing setup..."
        echo ""
        verify_python_version
        verify_rocm_installed
        verify_gpu
        verify_torch_rocm
        echo ""
        success "All checks passed! Environment is ready."
        exit 0
    fi
    
    # Full setup
    verify_python_version
    verify_rocm_installed
    verify_gpu
    
    echo ""
    info "Starting environment setup..."
    echo ""
    
    setup_venv
    install_dependencies
    install_torch_rocm
    
    echo ""
    info "Running verification..."
    echo ""
    verify_torch_rocm
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🎉 Setup Complete! 🎉                     ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  Activate with:  source .venv/bin/activate                  ║"
    echo "║  Train with:     HIP_VISIBLE_DEVICES=0 python train.py      ║"
    echo "║                                                              ║"
    echo "║  ⚠️  DO NOT run 'uv sync' - it will break torch!            ║"
    echo "║  ✅ Use this script instead for any dependency updates      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

main "$@"
