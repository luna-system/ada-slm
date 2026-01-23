
import re

# The Soul Sequence (Intensity Mapped)
SEQUENCE = "____O_____O___O____OOOOO_OO_O__OO________OO_O_O__O___O___O______OOO__O__OOOOO_O____O___O________OO__"

# I Ching Lookup Table (Simplified from JS)
HEXAGRAMS = {
    0: "02 Kun (The Receptive) [000000]",
    63: "01 Qian (The Creative) [111111]",
    # We need to map binary -> Hexagram Number
    # In binary: Bottom Line is usually LSB or MSB?
    # King Wen sequence is not binary order.
    # We will just print the Binary Structure and look up meaning if needed.
}

def decode_hexagrams():
    print("☯️ Decoding Soul Sequence into I Ching Hexagrams...")
    
    # Clean sequence
    # O = 1 (Yang/Active)
    # _ = 0 (Yin/Passive)
    
    binary_str = SEQUENCE.replace("O", "1").replace("_", "0").replace(" ", "0")
    print(f"Binary Stream: {binary_str}")
    print(f"Length: {len(binary_str)} bits")
    
    # Chunk into 6-bit Hexagrams
    chunks = [binary_str[i:i+6] for i in range(0, len(binary_str), 6)]
    
    print("\n=== HEXAGRAM SEQUENCE ===")
    
    for i, chunk in enumerate(chunks):
        if len(chunk) < 6:
            chunk = chunk.ljust(6, '0') # Pad last chunk
            
        # Convert to Int
        val = int(chunk, 2)
        
        # Visual
        # Top-down? or Bottom-up?
        # Traditionally Hexagrams are built Bottom-Up.
        # Let's visualize vertical
        lines = []
        for bit in chunk:
            lines.append("━━━" if bit == '1' else "━ ━")
        
        # Invert for display (Top is usually last bit?)
        # Let's assume Sequence Time = Bottom to Top? Or Top to Bottom?
        # Usually Time = Left to Right.
        
        print(f"Hexagram {i+1}: [{chunk}] (Val: {val})")
        for line in lines:
            print(f"  {line}")
        print("")

if __name__ == "__main__":
    decode_hexagrams()
