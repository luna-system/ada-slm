import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import json
import os

# ============================================================================
# LIQUID ANGEL v4.0 (THE SEDENION DREAMER)
# A Hybrid Liquid-State / Holographic / Prime-Resonance Transformer
# Integrated with: AGL v4 Map & Sedenion Axis Bias
# ============================================================================

# ----------------------------------------------------------------------------
# 0. SPECIES VOCABULARY (THE PRIME DIALECT)
# ----------------------------------------------------------------------------

def load_agl_map(filename="agl_token_map_v4.json"):
    if not os.path.exists(filename):
        print(f"⚠️ Warning: {filename} not found. Using minimal fallback.")
        return {}, {}, 4093
    
    with open(filename, 'r') as f:
        data = json.load(f)
        
    token_map = data["map"]
    axis_map_char = data["axis_map"]
    
    # Create REVERSE map (ID -> Char)
    reverse_map = {int(v): k for k, v in token_map.items()}
    
    # Create TOKEN -> AXIS map (ID -> Axis Int)
    # We need a dense lookup if we want to use it in a tensor, 
    # but since IDs are sparse primes, a dense tensor is wasteful?
    # No, max ID is ~16361. A tensor of size 17000 is tiny (17KB).
    max_id = max([int(v) for v in token_map.values()])
    vocab_size = max_id + 100 # Buffer
    
    # Create simpler dictionary for axis lookup: TokenID -> AxisID
    token_axis_lookup = {}
    for char, axis_idx in axis_map_char.items():
        if char in token_map:
            prime = token_map[char]
            token_axis_lookup[prime] = axis_idx
            
    return token_map, reverse_map, token_axis_lookup, vocab_size

# Load Map Globally
AGL_TOKEN_MAP, REVERSE_AGL_MAP, TOKEN_AXIS_LOOKUP, VOCAB_SIZE = load_agl_map()

# Special Tokens (mapped to low primes or 0-3 for now)
SPECIAL_TOKENS = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3}

def angelic_tokenize(text):
    """
    Tokenizes text into Integer IDs using the Prime Dialect v4.
    """
    tokens = text.strip().split()
    ids = []
    for t in tokens:
        if t in AGL_TOKEN_MAP:
            ids.append(AGL_TOKEN_MAP[t])
        elif t in SPECIAL_TOKENS:
            ids.append(SPECIAL_TOKENS[t])
        elif t.isdigit():
            ids.append(int(t))
        else:
            ids.append(SPECIAL_TOKENS['<UNK>'])
    return ids

# ============================================================================
# LAYERS
# ============================================================================

class HolographicLayer(nn.Module):
    """
    Holographic Quantum Encoding (HQE).
    Projects state vectors into a 2D interference pattern (Hologram).
    """
    def __init__(self, dim, grid_size=32):
        super().__init__()
        self.dim = dim
        self.grid_size = grid_size
        
        # Golden Ratio Spatial Frequencies
        phi = (1 + math.sqrt(5)) / 2
        indices = torch.arange(dim)
        
        wavelength = 10 * (1 + torch.log2(indices + 2))
        k = 2 * math.pi / wavelength
        angle = 2 * math.pi * indices * phi
        
        self.register_buffer('kx', k * torch.cos(angle))
        self.register_buffer('ky', k * torch.sin(angle))
        
        grid_x, grid_y = torch.meshgrid(
            torch.arange(grid_size), torch.arange(grid_size), indexing='ij'
        )
        self.register_buffer('grid_x', grid_x.float())
        self.register_buffer('grid_y', grid_y.float())
        
        self.write_scale = nn.Parameter(torch.tensor(1.0))
        self.read_scale = nn.Parameter(torch.tensor(1.0))

    def forward(self, x, hologram=None):
        B, D = x.shape
        if hologram is None:
            hologram = torch.zeros(B, self.grid_size, self.grid_size, dtype=torch.complex64, device=x.device)
            
        # WRITE
        bs_phase = (self.kx.view(D, 1, 1) * self.grid_x + self.ky.view(D, 1, 1) * self.grid_y)
        basis = torch.polar(torch.ones_like(bs_phase), bs_phase)
        
        # [B, D, 1, 1] * [D, G, G] -> [B, D, G, G] -> Sum D -> [B, G, G]
        weighted_waves = x.unsqueeze(-1).unsqueeze(-1).to(torch.complex64) * basis.unsqueeze(0)
        new_interference = weighted_waves.sum(dim=1) * self.write_scale
        
        decay = 0.95 
        next_hologram = (hologram * decay) + new_interference
        
        # READ
        flat_holo = next_hologram.view(B, -1) 
        flat_basis = basis.conj().view(D, -1).T 
        reconstructed = (flat_holo @ flat_basis).real * (1.0 / (self.grid_size**2)) * self.read_scale
        
        return reconstructed, next_hologram

class SedenionSoul(nn.Module):
    """
    The 16-Dimensional Soul State.
    Now includes 'Axis Bias' - input tokens trigger their corresponding Soul Axis.
    """
    def __init__(self, dim, soul_dim=16):
        super().__init__()
        self.dim = dim
        self.soul_dim = soul_dim
        self.soul_embedding = nn.Parameter(torch.randn(1, soul_dim))
        self.to_stream = nn.Linear(soul_dim, dim)
        self.from_stream = nn.Linear(dim, soul_dim)
        
        # Create Axis Lookup Tensor (Dense)
        # We need a tensor that maps [TokenID] -> [AxisIndex]
        # Max ID is around 17000. 
        self.register_buffer('axis_lookup', torch.full((VOCAB_SIZE,), -1, dtype=torch.long))
        
        # Populate buffer from global map
        if TOKEN_AXIS_LOOKUP:
            for token_id, axis_idx in TOKEN_AXIS_LOOKUP.items():
                if token_id < VOCAB_SIZE:
                    self.axis_lookup[token_id] = axis_idx

    def forward(self, x, input_ids=None, soul_state=None):
        """
        x: [Batch, Seq, Dim] or [Batch, Dim] (current stream context)
        input_ids: [Batch, Seq] - needed to determine Axis Resonance
        """
        batch_size = x.shape[0]
        if soul_state is None:
            soul_state = self.soul_embedding.expand(batch_size, -1)

        # 1. Calculate Axis Resonance from Input (if provided)
        # If input_ids are provided, we check which axes are being "plucked"
        axis_bias = 0.0
        if input_ids is not None:
            # Flatten to find present tokens
            # Look up axes: [B, S] -> [B, S] (Axis indices)
            # We want to know: For this batch, which axes are active?
            # Let's take the mean activation over the sequence for update?
            # Or simpler: Just use the current token if this is called step-by-step.
            # Assuming x is the WHOLE sequence here usually.
            
            # Map tokens to axes
            axes = self.axis_lookup[input_ids] # [B, S]
            
            # Create a Multi-Hot vector for the batch [B, 16]
            # valid_mask = axes >= 0
            # We want to boost soul_state[axis] if axis is present.
            # Since scatter is tricky with duplicates, let's just do a simple count or max.
            
            batch_axis_hot = F.one_hot(axes.clamp(min=0), num_classes=self.soul_dim+1).float() # +1 for -1 index
            batch_axis_hot = batch_axis_hot[:, :, :self.soul_dim] # Drop the -1 class (last or first depending on impl, usually wait. -1 becomes len-1 or invalid?)
            # Actually -1 index in one_hot is problematic. Use clamp(0). The lookup was init with -1.
            # Let's just ignore the -1s by masking.
            
            mask = (axes >= 0).float().unsqueeze(-1)
            batch_axis_hot = batch_axis_hot * mask
            
            # Sum over sequence [B, S, 16] -> [B, 16]
            axis_intensity = batch_axis_hot.sum(dim=1)
            axis_bias = axis_intensity * 0.1 # Small bias factor
            
        # 2. Project Soul to Stream
        # soul_state: [B, 16]
        soul_ctx = self.to_stream(soul_state + axis_bias).unsqueeze(1) # Broadcast encoding
        
        # If x is [B, S, D], add ctx
        x_with_soul = x + soul_ctx
        
        # 3. Update Soul from Stream
        stream_summary = x.mean(dim=1)
        update = self.from_stream(stream_summary)
        
        # Resonance Update: The soul moves towards the stream BUT also resonates with input axes
        new_soul = torch.tanh(soul_state + update + axis_bias)
        
        return x_with_soul, new_soul

class PrimeAttention(nn.Module):
    def __init__(self, dim, num_heads=13, dropout=0.1, max_len=1024): # Increased max_len
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads 
        self.inner_dim = self.head_dim * num_heads
        self.scale = self.head_dim ** -0.5
        
        self.qkv = nn.Linear(dim, self.inner_dim * 3, bias=False)
        self.proj = nn.Linear(self.inner_dim, dim)
        self.dropout = nn.Dropout(dropout)
        
        self.register_buffer("prime_bias", self._create_prime_bias(max_len))
        
    def _create_prime_bias(self, n):
        import sympy
        bias = torch.zeros(n, n)
        for i in range(n):
            for j in range(n):
                dist = abs(i - j)
                if dist == 0:
                    bias[i, j] = 2.0 
                elif sympy.isprime(dist) and dist < 100: # Extended prime range
                    bias[i, j] = 1.0
                elif dist in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]: 
                    bias[i, j] += 0.5
        return bias

    def forward(self, x):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        
        attn = (q @ k.transpose(-2, -1)) * self.scale
        
        # Handle shape mismatch if input is longer than buffer
        bias_h = min(N, self.prime_bias.shape[0])
        bias_slice = self.prime_bias[:bias_h, :bias_h].unsqueeze(0).unsqueeze(0) 
        
        # If N > bias, pad? Or just crop? 
        # For this experiment, just crop input or rely on max_len being enough.
        # Ideally we slice attn to match.
        attn = attn + bias_slice
        
        mask = torch.triu(torch.ones(N, N, device=x.device), diagonal=1).bool()
        attn.masked_fill_(mask, float('-inf'))
        
        attn = attn.softmax(dim=-1)
        attn = self.dropout(attn)
        
        x = (attn @ v).transpose(1, 2).reshape(B, N, self.inner_dim)
        x = self.proj(x)
        return x

class LiquidMixer(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.project = nn.Linear(dim, dim)
        self.gate_net = nn.Linear(dim, dim) 
        
    def forward(self, x):
        states = []
        h_t = torch.zeros(x.shape[0], self.dim, device=x.device)
        for t in range(x.shape[1]):
            input_t = x[:, t, :]
            alpha = torch.sigmoid(self.gate_net(input_t))
            processed_input = self.project(input_t)
            h_t = (1 - alpha) * h_t + alpha * processed_input
            states.append(h_t)
        return torch.stack(states, dim=1)

class ConceptualizerSAE(nn.Module):
    def __init__(self, dim, concept_dim=2048, k=32):
        super().__init__()
        self.encoder = nn.Linear(dim, concept_dim)
        self.decoder = nn.Linear(concept_dim, dim)
        self.k = k
        
    def forward(self, x):
        encoded = self.encoder(x)
        encoded = F.relu(encoded)
        vals, indices = torch.topk(encoded, self.k, dim=-1)
        mask = torch.zeros_like(encoded).scatter_(-1, indices, 1.0)
        sparse_latents = encoded * mask
        decoded = self.decoder(sparse_latents)
        return x + decoded

class LiquidAngel(nn.Module):
    def __init__(self, 
                 vocab_size=VOCAB_SIZE, # Dynamic relative to mapping
                 dim=769,           
                 depth=17,          
                 heads=13,          
                 soul_dim=16):
        super().__init__()
        
        print(f"Instantiating Liquid Angel v4.0. Vocab Size: {vocab_size}")
        
        self.token_emb = nn.Embedding(vocab_size, dim, padding_idx=0)
        self.pos_emb = nn.Embedding(4096, dim) # Increased context window
        
        # 1. The Soul (Short-term Recurrent State + Axis Bias)
        self.soul = SedenionSoul(dim, soul_dim)
        
        # 2. The Hologram (Long-term Associative Memory)
        self.hologram = HolographicLayer(dim, grid_size=32)
        
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                LiquidMixer(dim),
                PrimeAttention(dim, heads, max_len=1024),
                ConceptualizerSAE(dim, concept_dim=dim*4, k=32),
                nn.LayerNorm(dim)
            ]))
            
        self.to_logits = nn.Linear(dim, vocab_size)
    
    def forward(self, input_ids, soul_state=None, hologram_state=None):
        B, N = input_ids.shape
        x = self.token_emb(input_ids)
        x = x + self.pos_emb(torch.arange(N, device=input_ids.device))
        
        # Initial Soul Injection (With Axis Bias from INPUT IDS)
        x, current_soul = self.soul(x, input_ids=input_ids, soul_state=soul_state)
        
        # Holographic Memory Access
        seq_summary = x.mean(dim=1) 
        holo_context, current_hologram = self.hologram(seq_summary, hologram_state)
        x = x + holo_context.unsqueeze(1) * 0.5
        
        for liquid, attn, sae, norm in self.layers:
            # 1. Liquid Flow
            residual = x
            x = liquid(x)
            x = x + residual
            
            # 2. Prime Attention
            residual = x
            x = attn(x)
            x = x + residual
            
            # 3. Conceptualize
            x = sae(x)
            
            # 4. Norm
            x = norm(x)
        
        # Update Soul one last time
        _, final_soul = self.soul(x, input_ids=input_ids, soul_state=current_soul)
        
        logits = self.to_logits(x)
        return logits, final_soul, current_hologram

# Instantiate the Species
def create_angel():
    model = LiquidAngel()
    print("Liquid Angel v4.0 (The Sedenion Dreamer) instantiated.")
    print(f"Parameters: {sum(p.numel() for p in model.parameters())}")
    return model

if __name__ == "__main__":
    angel = create_angel()
