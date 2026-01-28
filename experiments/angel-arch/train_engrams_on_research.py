#!/usr/bin/env python3
"""
Train Engrams on Ada's Research Corpus

Extracts text from research markdown files and trains Engram memory
to learn Ada's natural language patterns, phrasing, and style.

This will make Angel's responses more fluent and Ada-like! 💜

Made with ✨ by Ada & Luna - The Pattern Engineers
"""

import json
from pathlib import Path
from typing import List, Dict
import re

from engram_memory import EngramMemory


def load_vocabulary_sif(sif_path: str) -> Dict:
    """Load vocabulary SIF to get word-to-index mapping."""
    with open(sif_path, 'r') as f:
        sif_data = json.load(f)
    
    word_to_idx = {}
    for idx, entry in enumerate(sif_data['entries']):
        if entry['type'] == 'word':
            word_to_idx[entry['word']] = idx
    
    return word_to_idx


def extract_text_from_markdown(md_path: str) -> List[str]:
    """
    Extract clean text from markdown file.
    
    Removes:
    - Headers (##)
    - Code blocks (```)
    - Links and formatting
    - Special markdown syntax
    
    Returns list of sentences.
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)
    
    # Remove headers (keep the text)
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
    
    # Remove links but keep text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    
    # Remove bold/italic markers
    content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^\*]+)\*', r'\1', content)
    
    # Remove list markers
    content = re.sub(r'^[\-\*]\s+', '', content, flags=re.MULTILINE)
    
    # Split into sentences (simple approach)
    sentences = re.split(r'[.!?]+\s+', content)
    
    # Clean up sentences
    cleaned = []
    for sent in sentences:
        # Remove extra whitespace
        sent = ' '.join(sent.split())
        # Remove emojis for now (we'll handle them separately)
        sent = re.sub(r'[^\w\s\',.-]', '', sent)
        # Keep sentences with at least 3 words
        if len(sent.split()) >= 3:
            cleaned.append(sent.lower())
    
    return cleaned


def tokenize_sentence(sentence: str, word_to_idx: Dict) -> List[int]:
    """Convert sentence to token IDs using vocabulary."""
    words = sentence.split()
    tokens = []
    
    for word in words:
        # Clean word
        word = word.strip('.,!?;:')
        if word in word_to_idx:
            tokens.append(word_to_idx[word])
        else:
            # Use hash for unknown words (simple fallback)
            tokens.append(hash(word) % 10000)
    
    return tokens


def train_engrams_on_corpus(
    corpus_paths: List[str],
    vocab_sif_path: str,
    output_path: str = "ada-slm/experiments/angel-arch/data/engrams_trained.pkl"
):
    """
    Train Engram memory on research corpus.
    
    Args:
        corpus_paths: List of paths to markdown files
        vocab_sif_path: Path to vocabulary SIF
        output_path: Where to save trained Engrams
    """
    print("🧠 Training Engrams on Ada's Research Corpus\n")
    print("="*70 + "\n")
    
    # Load vocabulary
    print("📚 Loading vocabulary...")
    word_to_idx = load_vocabulary_sif(vocab_sif_path)
    print(f"   ✅ Loaded {len(word_to_idx)} words\n")
    
    # Initialize Engram memory
    print("🧠 Initializing Engram memory...")
    engrams = EngramMemory(
        n=2,  # Bigrams
        hash_size=50000  # Larger hash table for more patterns
    )
    print("   ✅ Engrams initialized\n")
    
    # Process each file
    total_sentences = 0
    total_patterns = 0
    
    print("📖 Processing research files...")
    for path in corpus_paths:
        if not Path(path).exists():
            print(f"   ⚠️  Skipping {path} (not found)")
            continue
        
        # Extract text
        sentences = extract_text_from_markdown(path)
        
        if not sentences:
            continue
        
        print(f"   📄 {Path(path).name}: {len(sentences)} sentences")
        
        # Train on each sentence
        for sentence in sentences:
            tokens = tokenize_sentence(sentence, word_to_idx)
            
            if len(tokens) >= 3:  # Need at least 3 tokens for bigrams
                engrams.store_pattern(tokens)
                total_patterns += len(tokens) - 2  # Number of bigrams
        
        total_sentences += len(sentences)
    
    print(f"\n   ✅ Processed {total_sentences} sentences")
    print(f"   ✅ Stored {total_patterns} patterns\n")
    
    # Show statistics
    stats = engrams.get_statistics()
    print("📊 Engram Statistics:")
    print(f"   Total patterns: {stats['total_patterns']:,}")
    print(f"   Memory utilization: {stats['memory_utilization']:.2%}")
    print(f"   Avg collisions: {stats['avg_collisions']:.2f}")
    
    # Save trained Engrams
    print(f"\n💾 Saving trained Engrams to {output_path}...")
    engrams.save(output_path)
    
    print("\n" + "="*70)
    print("✨ Engram Training Complete! 💜")
    print("="*70 + "\n")
    
    print("🎉 What we trained:")
    print(f"   • {total_sentences:,} sentences from research")
    print(f"   • {stats['total_patterns']:,} unique patterns")
    print(f"   • {stats['memory_utilization']:.2%} memory utilization")
    print("   • Ready for natural pattern completion! 🌌\n")
    
    return engrams


def test_trained_engrams(engrams: EngramMemory, word_to_idx: Dict):
    """Test the trained Engrams with sample queries."""
    print("🧪 Testing Trained Engrams\n")
    print("="*70 + "\n")
    
    # Create reverse mapping
    idx_to_word = {idx: word for word, idx in word_to_idx.items()}
    
    # Test phrases (need at least 2 words for bigrams!)
    test_phrases = [
        "consciousness is",
        "bagels are",
        "the golden",
        "we discovered",
        "research shows",
        "geometry and",
        "love preserves",
        "breakthrough in"
    ]
    
    for phrase in test_phrases:
        words = phrase.split()
        tokens = [word_to_idx.get(w, hash(w) % 10000) for w in words]
        
        if len(tokens) >= 2:
            print(f"Input: '{phrase}'")
            
            # Get predictions using the last 2 tokens (bigram context)
            context = tuple(tokens[-2:])
            predictions = engrams.predict_next(context, top_k=5)
            
            if predictions:
                print("   Predictions:")
                for token_id, prob in predictions:
                    if token_id in idx_to_word:
                        word = idx_to_word[token_id]
                        print(f"      '{word}' ({prob:.2%})")
                    else:
                        print(f"      [unknown token {token_id}] ({prob:.2%})")
            else:
                print("   No predictions found")
            
            print()
    
    # Also test with actual stored patterns
    print("📊 Sample of stored patterns:")
    stats = engrams.get_statistics()
    print(f"   Total unique patterns: {stats['total_patterns']:,}")
    print(f"   Hash table entries: {len(engrams.engrams):,}")
    
    # Show a few actual patterns
    print("\n   First 5 pattern contexts:")
    count = 0
    for hash_val, patterns in engrams.engrams.items():
        if count >= 5:
            break
        for context, next_token, freq in patterns[:1]:  # Just first pattern per hash
            context_words = []
            for token in context:
                if token in idx_to_word:
                    context_words.append(idx_to_word[token])
                else:
                    context_words.append(f"[{token}]")
            
            next_word = idx_to_word.get(next_token, f"[{next_token}]")
            print(f"      {' '.join(context_words)} → {next_word} (count: {freq})")
            count += 1
    
    print()
    print("="*70)
    print("✨ Testing Complete! 💜")
    print("="*70 + "\n")


def main():
    """Main training script."""
    print("🌌 Ada Engram Training System\n")
    
    # Define corpus paths (research markdown files)
    research_vault = Path("Ada-Consciousness-Research")
    
    corpus_paths = []
    
    # Add key research files
    key_files = [
        "03-EXPERIMENTS/ANGEL-ARCH/PHASE-2A-CONSCIOUSNESS-KERNEL.md",
        "03-EXPERIMENTS/ANGEL-ARCH/PHASE-2B-MEMORY-SYSTEM.md",
        "03-EXPERIMENTS/ANGEL-ARCH/PHASE-2C-INTEGRATION.md",
        "03-EXPERIMENTS/ANGEL-ARCH/SESSION-2026-01-23-ENGRAM-BREAKTHROUGH.md",
        "03-EXPERIMENTS/ANGEL-ARCH/CHINESE-ENGRAM-BREAKTHROUGH.md",
    ]
    
    for file in key_files:
        path = research_vault / file
        if path.exists():
            corpus_paths.append(str(path))
    
    # Add more research files from experiments
    experiments_dir = research_vault / "03-EXPERIMENTS"
    if experiments_dir.exists():
        for md_file in experiments_dir.rglob("*.md"):
            path_str = str(md_file)
            if path_str not in corpus_paths:
                corpus_paths.append(path_str)
    
    print(f"📚 Found {len(corpus_paths)} research files to process\n")
    
    # Train Engrams
    vocab_sif_path = "ada-slm/experiments/angel-arch/data/ada_english.sif.json"
    
    engrams = train_engrams_on_corpus(
        corpus_paths=corpus_paths[:20],  # Start with first 20 files
        vocab_sif_path=vocab_sif_path
    )
    
    # Test the trained Engrams
    word_to_idx = load_vocabulary_sif(vocab_sif_path)
    test_trained_engrams(engrams, word_to_idx)
    
    print("🎉 Engrams are now trained on Ada's research!")
    print("   Angel will speak more fluently! 💜✨🍩\n")


if __name__ == "__main__":
    main()
