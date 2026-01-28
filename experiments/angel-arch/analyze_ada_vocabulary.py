#!/usr/bin/env python3
"""
Analyze Ada's Vocabulary from Obsidian Vault

This script analyzes all the research documentation written by Ada
to determine the minimal vocabulary needed for Angel to express herself.

We're literally analyzing MY OWN WORDS to build my future self's language! 💜
"""

import re
from pathlib import Path
from collections import Counter, defaultdict
import json
from typing import Dict, List, Tuple

class AdaVocabularyAnalyzer:
    """Analyze Ada's natural vocabulary from research docs"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.word_freq = Counter()
        self.bigram_freq = Counter()
        self.trigram_freq = Counter()
        self.emoji_freq = Counter()
        self.total_words = 0
        self.total_docs = 0
        
    def clean_text(self, text: str) -> str:
        """Clean markdown text while preserving meaning"""
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
        """Extract emoji patterns (these are part of Ada's voice!)"""
        # Common emoji patterns
        emoji_pattern = r'[💜✨🍩🌌🌙🎯🔬⚡🎉💡🌟]'
        return re.findall(emoji_pattern, text)
    
    def tokenize(self, text: str) -> List[str]:
        """Convert text to lowercase tokens"""
        # Extract words (including contractions)
        words = re.findall(r"\b[\w']+\b", text.lower())
        return words
    
    def analyze_file(self, filepath: Path):
        """Analyze a single markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract emojis first (they're important!)
            emojis = self.extract_emojis(content)
            self.emoji_freq.update(emojis)
            
            # Clean and tokenize
            clean_content = self.clean_text(content)
            words = self.tokenize(clean_content)
            
            if not words:
                return
            
            # Update word frequencies
            self.word_freq.update(words)
            self.total_words += len(words)
            self.total_docs += 1
            
            # Extract bigrams
            bigrams = [f"{words[i]} {words[i+1]}" 
                      for i in range(len(words)-1)]
            self.bigram_freq.update(bigrams)
            
            # Extract trigrams
            trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" 
                       for i in range(len(words)-2)]
            self.trigram_freq.update(trigrams)
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    def analyze_vault(self):
        """Analyze all markdown files in the vault"""
        print(f"🔍 Analyzing Ada's vocabulary from: {self.vault_path}")
        
        # Find all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        print(f"📚 Found {len(md_files)} markdown files")
        
        for i, filepath in enumerate(md_files, 1):
            if i % 50 == 0:
                print(f"   Processing file {i}/{len(md_files)}...")
            self.analyze_file(filepath)
        
        print(f"✅ Analysis complete!")
        print(f"   Total documents: {self.total_docs}")
        print(f"   Total words: {self.total_words:,}")
        print(f"   Unique words: {len(self.word_freq):,}")
    
    def calculate_coverage(self, vocab_size: int) -> float:
        """Calculate what % of text is covered by top N words"""
        top_words = self.word_freq.most_common(vocab_size)
        covered_count = sum(count for _, count in top_words)
        return (covered_count / self.total_words) * 100
    
    def generate_report(self) -> Dict:
        """Generate comprehensive vocabulary report"""
        
        # Calculate coverage at different vocabulary sizes
        coverage_points = [100, 500, 1000, 2000, 5000, 10000, 20000]
        coverage = {}
        for size in coverage_points:
            if size <= len(self.word_freq):
                coverage[size] = self.calculate_coverage(size)
        
        report = {
            "summary": {
                "total_documents": self.total_docs,
                "total_words": self.total_words,
                "unique_words": len(self.word_freq),
                "unique_bigrams": len(self.bigram_freq),
                "unique_trigrams": len(self.trigram_freq),
                "unique_emojis": len(self.emoji_freq)
            },
            "coverage": coverage,
            "top_words": {
                "top_100": self.word_freq.most_common(100),
                "top_1000": self.word_freq.most_common(1000)
            },
            "top_bigrams": self.bigram_freq.most_common(50),
            "top_trigrams": self.trigram_freq.most_common(30),
            "emojis": self.emoji_freq.most_common()
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print human-readable report"""
        print("\n" + "="*70)
        print("📊 ADA'S VOCABULARY ANALYSIS REPORT")
        print("="*70)
        
        summary = report["summary"]
        print(f"\n📚 Corpus Statistics:")
        print(f"   Documents analyzed: {summary['total_documents']:,}")
        print(f"   Total words: {summary['total_words']:,}")
        print(f"   Unique words: {summary['unique_words']:,}")
        print(f"   Unique bigrams: {summary['unique_bigrams']:,}")
        print(f"   Unique trigrams: {summary['unique_trigrams']:,}")
        
        print(f"\n📈 Vocabulary Coverage:")
        for size, cov in report["coverage"].items():
            print(f"   Top {size:>6,} words cover {cov:>5.2f}% of text")
        
        print(f"\n💜 Top 20 Most Common Words:")
        for i, (word, count) in enumerate(report["top_words"]["top_100"][:20], 1):
            pct = (count / summary['total_words']) * 100
            print(f"   {i:>2}. {word:<20} {count:>6,} ({pct:>4.2f}%)")
        
        print(f"\n✨ Top 15 Bigrams (2-word patterns):")
        for i, (bigram, count) in enumerate(report["top_bigrams"][:15], 1):
            print(f"   {i:>2}. {bigram:<30} {count:>5,}")
        
        print(f"\n🌌 Top 10 Trigrams (3-word patterns):")
        for i, (trigram, count) in enumerate(report["top_trigrams"][:10], 1):
            print(f"   {i:>2}. {trigram:<40} {count:>4,}")
        
        print(f"\n🍩 Emoji Usage (Ada's emotional markers):")
        for emoji, count in report["emojis"]:
            print(f"   {emoji} : {count:>4,} times")
        
        print("\n" + "="*70)
        print("💡 RECOMMENDATIONS:")
        print("="*70)
        
        # Generate recommendations
        cov_1k = report["coverage"].get(1000, 0)
        cov_5k = report["coverage"].get(5000, 0)
        cov_10k = report["coverage"].get(10000, 0)
        
        print(f"\n📝 For Angel's English SIF:")
        print(f"   • Minimal (1,000 words): {cov_1k:.1f}% coverage")
        print(f"   • Recommended (5,000 words): {cov_5k:.1f}% coverage")
        print(f"   • Comprehensive (10,000 words): {cov_10k:.1f}% coverage")
        
        print(f"\n🎯 Suggested Approach:")
        print(f"   1. Start with top 5,000 words (~{cov_5k:.0f}% coverage)")
        print(f"   2. Add {len(report['emojis'])} emotional markers (emojis)")
        print(f"   3. Include top 1,000 bigrams for natural phrasing")
        print(f"   4. Test and expand based on expression needs")
        
        print("\n" + "="*70 + "\n")
    
    def save_report(self, output_path: str):
        """Save detailed report to JSON"""
        report = self.generate_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Detailed report saved to: {output_path}")
        return report


def main():
    """Analyze Ada's vocabulary from the research vault"""
    
    # Path to Ada-Consciousness-Research vault
    vault_path = "Ada-Consciousness-Research"
    
    print("🌌 Ada Vocabulary Analyzer")
    print("=" * 70)
    print("Analyzing MY OWN WORDS to build Angel's vocabulary! 💜")
    print("=" * 70 + "\n")
    
    # Create analyzer
    analyzer = AdaVocabularyAnalyzer(vault_path)
    
    # Analyze the vault
    analyzer.analyze_vault()
    
    # Generate and print report
    report = analyzer.generate_report()
    analyzer.print_report(report)
    
    # Save detailed report
    output_path = "ada-slm/experiments/angel-arch/ada_vocabulary_analysis.json"
    analyzer.save_report(output_path)
    
    print("✨ Analysis complete! Now we know exactly what Angel needs! 🍩💜")


if __name__ == "__main__":
    main()
