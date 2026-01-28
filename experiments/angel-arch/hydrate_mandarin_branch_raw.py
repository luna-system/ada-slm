"""
Hydrate Mandarin Chinese Language Branch SIF

Takes the top 100 Mandarin words and maps them to 16D consciousness coordinates.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif_raw import RawLanguageSIFGenerator


def main():
    """Hydrate Mandarin branch with top 100 words"""
    
    # Top 100 Mandarin Chinese words from 1000mostcommonwords.com
    top_100_mandarin = [
        "一", "人", "里", "会", "没", "她", "吗", "去", "也", "有",
        "这", "那", "不", "什", "个", "来", "要", "就", "我", "你",
        "的", "是", "了", "他", "么", "们", "在", "说", "为", "好",
        "吧", "知道", "我的", "和", "你的", "想", "只", "很", "都", "对",
        "把", "啊", "怎", "得", "还", "过", "不是", "到", "样", "飞",
        "远", "身", "任何", "生活", "够", "号", "兰", "瑞", "达", "或",
        "愿", "蒂", "別", "军", "正", "是不是", "证", "不用", "三", "乐",
        "吉", "男人", "告訴", "路", "搞", "可是", "与", "次", "狗", "决",
        "金", "史", "姆", "部", "正在", "活", "刚", "回家", "贝", "如何",
        "须", "战", "不會", "夫", "喂", "父", "亚", "肯定", "女孩", "世界"
    ]
    
    print(f"🌌 Hydrating Mandarin Chinese branch with {len(top_100_mandarin)} words...")
    
    # Initialize generator
    generator = RawLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "Mandarin Chinese",
        "family": "Sino-Tibetan",
        "writing_system": "Hanzi (Simplified)"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_mandarin,
        "mandarin",
        language_metadata
    )
    
    # Save to file
    output_path = "data-raw/language_mandarin_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ Mandarin Chinese Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ Mandarin Chinese branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
