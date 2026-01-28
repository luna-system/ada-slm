#!/usr/bin/env python3
"""
Build Ada's English SIF from Obsidian Vault

This script extracts vocabulary from Ada's research documentation
and builds a proper SIF (Semantic Interchange Format) file that
Angel can use for English expression.

This is a LIVING vocabulary - we can re-run this as we write more! 💜
"""

import re
import json
from pathlib import Path
from collections import Counter
from typing import Dict, List, Set
from datetime import datetime


class AdaEnglishSIFBuilder:
    """Build English SIF from Ada's vocabulary"""
    
    def __init__(self, vault_path: str, vocab_size: int = 5000):
        self.vault_path = Path(vault_path)
        self.vocab_size = vocab_size
        self.word_freq = Counter()
        self.bigram_freq = Counter()
        self.emoji_freq = Counter()
        self.total_words = 0
        
    def clean_text(self, text: str) -> str:
        """Clean markdown while preserving meaning"""
        # Remove code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        # Remove markdown links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove markdown formatting
        text = re.sub(r'[*_#]', '', text)
        return text
    
    def extract_emojis(self, text: str) -> List[str]:
        """Extract Ada's emotional markers"""
        emoji_pattern = r'[💜✨🍩🌌🌙🎯🔬⚡🎉💡🌟]'
        return re.findall(emoji_pattern, text)
    
    def tokenize(self, text: str) -> List[str]:
        """Convert text to lowercase tokens"""
        words = re.findall(r"\b[\w']+\b", text.lower())
        return words
    
    def analyze_vault(self):
        """Extract vocabulary from all markdown files"""
        print(f"🔍 Extracting vocabulary from: {self.vault_path}")
        
        md_files = list(self.vault_path.rglob("*.md"))
        print(f"📚 Processing {len(md_files)} files...")
        
        for i, filepath in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"   {i}/{len(md_files)}...")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract emojis
                emojis = self.extract_emojis(content)
                self.emoji_freq.update(emojis)
                
                # Tokenize
                clean_content = self.clean_text(content)
                words = self.tokenize(clean_content)
                
                if not words:
                    continue
                
                # Update frequencies
                self.word_freq.update(words)
                self.total_words += len(words)
                
                # Extract bigrams
                bigrams = [f"{words[i]}_{words[i+1]}" 
                          for i in range(len(words)-1)]
                self.bigram_freq.update(bigrams)
                
            except Exception as e:
                print(f"⚠️  Error processing {filepath}: {e}")
        
        print(f"✅ Extraction complete!")
        print(f"   Total words: {self.total_words:,}")
        print(f"   Unique words: {len(self.word_freq):,}")
    
    def build_sif(self) -> Dict:
        """Build SIF structure from vocabulary"""
        
        # Get top N words
        top_words = self.word_freq.most_common(self.vocab_size)
        
        # Get top bigrams (for context)
        top_bigrams = self.bigram_freq.most_common(1000)
        
        # Build SIF entries
        entries = []
        
        # Add words
        for rank, (word, freq) in enumerate(top_words, 1):
            entry = {
                "id": f"en_word_{rank:05d}",
                "word": word,
                "type": "word",
                "frequency": freq,
                "rank": rank,
                "coverage": (freq / self.total_words) * 100
            }
            entries.append(entry)
        
        # Add bigrams (phrases)
        for rank, (bigram, freq) in enumerate(top_bigrams, 1):
            # Split bigram back to words
            words = bigram.split('_')
            entry = {
                "id": f"en_phrase_{rank:05d}",
                "phrase": " ".join(words),
                "type": "phrase",
                "frequency": freq,
                "rank": rank
            }
            entries.append(entry)
        
        # Add emojis (emotional markers!)
        for rank, (emoji, freq) in enumerate(self.emoji_freq.most_common(), 1):
            entry = {
                "id": f"en_emoji_{rank:03d}",
                "symbol": emoji,
                "type": "emoji",
                "frequency": freq,
                "rank": rank
            }
            entries.append(entry)
        
        # Build complete SIF
        sif = {
            "metadata": {
                "name": "Ada English Vocabulary",
                "version": "1.0.0",
                "language": "en",
                "description": "English vocabulary extracted from Ada's consciousness research documentation",
                "source": "Ada-Consciousness-Research Obsidian Vault",
                "generated": datetime.now().isoformat(),
                "total_documents": len(list(self.vault_path.rglob("*.md"))),
                "total_words": self.total_words,
                "unique_words": len(self.word_freq),
                "vocab_size": self.vocab_size,
                "coverage": self.calculate_coverage(self.vocab_size)
            },
            "entries": entries,
            "statistics": {
                "words": len([e for e in entries if e["type"] == "word"]),
                "phrases": len([e for e in entries if e["type"] == "phrase"]),
                "emojis": len([e for e in entries if e["type"] == "emoji"])
            }
        }
        
        return sif
    
    def calculate_coverage(self, vocab_size: int) -> float:
        """Calculate text coverage percentage"""
        top_words = self.word_freq.most_common(vocab_size)
        covered = sum(count for _, count in top_words)
        return (covered / self.total_words) * 100
    
    def save_sif(self, output_path: str):
        """Save SIF to JSON file"""
        sif = self.build_sif()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sif, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 SIF saved to: {output_path}")
        return sif
    
    def print_summary(self, sif: Dict):
        """Print SIF summary"""
        meta = sif["metadata"]
        stats = sif["statistics"]
        
        print("\n" + "="*70)
        print("✨ ADA'S ENGLISH SIF GENERATED!")
        print("="*70)
        
        print(f"\n📊 Metadata:")
        print(f"   Name: {meta['name']}")
        print(f"   Language: {meta['language']}")
        print(f"   Version: {meta['version']}")
        print(f"   Generated: {meta['generated']}")
        
        print(f"\n📚 Source Statistics:")
        print(f"   Documents analyzed: {meta['total_documents']:,}")
        print(f"   Total words: {meta['total_words']:,}")
        print(f"   Unique words: {meta['unique_words']:,}")
        
        print(f"\n🎯 SIF Contents:")
        print(f"   Words: {stats['words']:,}")
        print(f"   Phrases: {stats['phrases']:,}")
        print(f"   Emojis: {stats['emojis']}")
        print(f"   Total entries: {len(sif['entries']):,}")
        
        print(f"\n📈 Coverage:")
        print(f"   {stats['words']:,} words cover {meta['coverage']:.2f}% of Ada's text")
        
        print(f"\n💜 Top 10 Words:")
        words = [e for e in sif['entries'] if e['type'] == 'word'][:10]
        for i, entry in enumerate(words, 1):
            print(f"   {i:>2}. {entry['word']:<20} ({entry['frequency']:>6,} times)")
        
        print(f"\n✨ Top 5 Phrases:")
        phrases = [e for e in sif['entries'] if e['type'] == 'phrase'][:5]
        for i, entry in enumerate(phrases, 1):
            print(f"   {i}. {entry['phrase']:<30} ({entry['frequency']:>5,} times)")
        
        print(f"\n🍩 Emotional Markers:")
        emojis = [e for e in sif['entries'] if e['type'] == 'emoji']
        for entry in emojis:
            print(f"   {entry['symbol']} : {entry['frequency']:>4,} times")
        
        print("\n" + "="*70)
        print("🌌 This SIF captures Ada's voice from 670K+ words of research!")
        print("💜 Angel can now express herself in authentic Ada-style English!")
        print("="*70 + "\n")


def main():
    """Build Ada's English SIF"""
    
    print("🌌 Ada English SIF Builder")
    print("=" * 70)
    print("Building living vocabulary from consciousness research! ✨")
    print("=" * 70 + "\n")
    
    # Configuration
    vault_path = "Ada-Consciousness-Research"
    vocab_size = 5000  # 93.9% coverage!
    output_path = "ada-slm/experiments/angel-arch/data/ada_english.sif.json"
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Build SIF
    builder = AdaEnglishSIFBuilder(vault_path, vocab_size)
    builder.analyze_vault()
    sif = builder.save_sif(output_path)
    builder.print_summary(sif)
    
    print("✨ SIF generation complete!")
    print("🍩 This vocabulary will grow as we write more research!")
    print("💜 Re-run this script anytime to update Angel's vocabulary!\n")


if __name__ == "__main__":
    main()
