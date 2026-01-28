"""
Hydrate Korean Language Branch (RAW - No Hashing) SIF

Takes the top 100 Korean words and maps them to 16D consciousness coordinates.

Authors: Ada & Luna (Ada Consciousness Research Initiative)
Date: January 23, 2026
"""

import json
from generate_language_sif_raw import RawLanguageSIFGenerator


def main():
    """Hydrate Korean branch with top 100 words"""
    
    # Top 100 Korean words from National Institute of Korean Language (via flexiclasses.com)
    top_100_korean = [
        "것", "하다", "있다", "되다", "수", "나", "그", "없다", "않다", "사람",
        "우리", "이", "아니다", "보다", "등", "때", "거", "같다", "주다", "대하다",
        "가다", "년", "한", "말", "일", "이", "때문", "말하다", "위하다", "그러나",
        "오다", "알다", "씨", "그렇다", "크다", "또", "사회", "많다", "안", "좋다",
        "더", "받다", "그것", "집", "나오다", "따르다", "그리고", "문제", "그런", "살다",
        "저", "못하다", "생각하다", "모르다", "속", "만들다", "데", "두", "앞", "경우",
        "중", "어떤", "잘", "그녀", "먹다", "오다", "자신", "문화", "원", "생각",
        "어떻다", "명", "통하다", "그러다", "소리", "다시", "다른", "이런", "여자", "개",
        "정도", "뒤", "듣다", "다", "좀", "들다", "싶다", "보이다", "가지다", "함께",
        "아이", "지나다", "많이", "시간", "너", "인간", "사실", "나다", "이렇다", "학교"
    ]
    
    print(f"🌌 Hydrating Korean branch with {len(top_100_korean)} words...")
    
    # Initialize generator
    generator = RawLanguageSIFGenerator()
    
    # Language metadata
    language_metadata = {
        "name": "Korean",
        "family": "Koreanic",
        "writing_system": "Hangul"
    }
    
    # Generate complete branch SIF
    branch_sif = generator.generate_language_branch_sif(
        top_100_korean,
        "korean",
        language_metadata
    )
    
    # Save to file
    output_path = "data-raw/language_korean_branch.sif.json"
    generator.save_sif_file(branch_sif, output_path)
    
    # Print statistics
    print(f"\n✨ Korean Branch Statistics:")
    print(f"  Total words: {branch_sif['statistics']['word_count']}")
    print(f"  Average frequency: {branch_sif['statistics']['average_frequency']:.3f} Hz")
    print(f"\n🎯 Consciousness Coverage:")
    
    coverage = branch_sif['statistics']['consciousness_coverage']
    sorted_coverage = sorted(coverage.items(), key=lambda x: x[1], reverse=True)
    
    for axis, percent in sorted_coverage[:10]:  # Top 10
        if percent > 0:
            print(f"  {axis:15s}: {percent:6.1%}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"✅ Korean branch hydration complete! 🍩✨")


if __name__ == "__main__":
    main()
