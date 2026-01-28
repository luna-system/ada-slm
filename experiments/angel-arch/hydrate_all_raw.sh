#!/bin/bash
# Hydrate all 10 languages with RAW (no hashing) values

echo "🌍 Hydrating ALL languages with RAW character values"
echo "======================================================"
echo ""

languages=("english" "spanish" "mandarin" "arabic" "japanese" "hindi" "swahili" "russian" "korean" "quechua")

for lang in "${languages[@]}"; do
    echo "🔄 Processing $lang..."
    uv run python "hydrate_${lang}_branch_raw.py"
    echo ""
done

echo "✅ All languages hydrated with RAW values!"
echo "📁 Output: data-raw/"
