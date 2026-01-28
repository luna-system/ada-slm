"""
Hydrate Japanese Language Branch (RAW - No Hashing) SIF

Takes the top 100 Japanese words and maps them to 16D consciousness coordinates.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif_raw import RawLanguageSIFGenerator


def main():
    """Hydrate Japanese branch with top 100 words"""
    
    # Top 100 Japanese words from Wiktionary analysis (via flexiclasses.com)
    top_100_japanese = [
        "の", "に", "する", "は", "を", "が", "と", "年", "で", "だ",
        "月", "も", "から", "日", "成る", "こと", "有る", "よる", "や", "など",
        "言う", "日本", "為", "この", "人", "その", "まで", "もの", "へ", "又",
        "これ", "行う", "よう", "出来る", "駅", "国", "より", "大学", "現在", "後",
        "か", "線", "ぬ", "放送", "号", "軍", "無い", "部", "持つ", "所",
        "名", "回", "世界", "時", "戦", "時代", "東京", "おく", "でも", "呼ぶ",
        "その後", "会", "それ", "機", "会う", "受ける", "多い", "選手", "場合", "対する",
        "しかし", "つく", "昭和", "作品", "地", "中", "使用", "共に", "学校", "語",
        "彼", "行く", "アメリカ", "当時", "番組", "車", "社", "川", "映画", "位",
        "見る", "テレビ", "系", "研究", "町", "東", "存在", "活動", "発売", "他"
    ]
    
    print(f"🌌 Hydrating Japanese branch with {len(top_100_japanese)} words...")
    
    # Initialize generator
    generator = RawLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "Japanese",
        "family": "Japonic",
        "writing_system": "Kanji/Hiragana/Katakana"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_japanese,
        "japanese",
        language_metadata
    )
    
    # Save to file
    output_path = "data-raw/language_japanese_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ Japanese Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ Japanese branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
