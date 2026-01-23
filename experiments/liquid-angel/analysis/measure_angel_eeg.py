
import numpy as np
import os
import glob
from PIL import Image
import matplotlib.pyplot as plt

# CONFIG
ARTIFACTS_DIR = "forge_v4_artifacts/probes"
OUTPUT_FILE = "angel_eeg_spectrum.png"

def measure_eeg():
    print("🧠 Measuring Angelic EEG (Flux Spectral Analysis)...")
    
    # 1. Load Frames
    # We use the 16D probes (Simulated Sedenion State)
    files = sorted(glob.glob(os.path.join(ARTIFACTS_DIR, "*_16D.png")))
    
    if not files:
        print("No probe files found.")
        return

    print(f"Found {len(files)} frames.")
    
    flux_signal = []
    
    # 2. Calculate Flux (Frame-to-Frame Difference)
    prev_arr = None
    
    for i, f in enumerate(files):
        try:
            img = Image.open(f).convert("L") # Grayscale
            arr = np.array(img, dtype=np.float32)
            
            if prev_arr is not None:
                # Flux = Mean Absolute Difference
                diff = np.abs(arr - prev_arr)
                flux = np.mean(diff)
                flux_signal.append(flux)
            
            prev_arr = arr
            
            if i % 100 == 0:
                print(f"Processing step {i}...")
                
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    flux_signal = np.array(flux_signal)
    
    # 3. Spectral Analysis (FFT)
    # Sampling rate = 1 Step. Frequency unit = "Cycles per Step"
    freqs = np.fft.rfft(flux_signal)
    magnitudes = np.abs(freqs)
    
    # x-axis for plot
    n = len(flux_signal)
    freq_bins = np.fft.rfftfreq(n, d=1.0) # d=1 step
    
    # 4. Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Raw Flux Signal (Time Domain)
    ax1.plot(flux_signal, color='cyan', alpha=0.8, linewidth=1)
    ax1.set_title("Angel's Flux Signal (Time Domain)")
    ax1.set_xlabel("Time (Steps)")
    ax1.set_ylabel("Global Flux (Change Magnitude)")
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Power Spectrum (Frequency Domain)
    # Ignore DC component (index 0)
    ax2.plot(freq_bins[1:], magnitudes[1:], color='magenta')
    ax2.set_title("Spectral Power Density (Angelic EEG)")
    ax2.set_xlabel("Frequency (Cycles per Step)")
    ax2.set_ylabel("Power")
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log') # Log scale often reveals brainwaves better
    
    # Find Peaks
    peak_idx = np.argmax(magnitudes[1:]) + 1
    peak_freq = freq_bins[peak_idx]
    peak_period = 1.0 / peak_freq
    
    print(f"\n🏆 DOMINANT FREQUENCY: {peak_freq:.4f} cycles/step")
    print(f"⏱️ DOMINANT PERIOD: {peak_period:.2f} steps")
    
    ax2.axvline(peak_freq, color='yellow', linestyle='--', label=f'Peak: {peak_period:.1f} steps')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    print(f"Saved EEG analysis to {OUTPUT_FILE}")

if __name__ == "__main__":
    measure_eeg()
