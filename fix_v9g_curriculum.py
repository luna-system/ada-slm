#!/usr/bin/env python3
"""
Fix the v9g curriculum training script to work with messages format.
Quick patch to get training running.
"""

def fix_tokenize_function():
    """Update the tokenization function in the training script."""
    
    # Read the original script
    with open("train_v9g_curriculum.py", "r") as f:
        content = f.read()
    
    # Replace the problematic tokenize function
    old_tokenize = '''    def tokenize_function(examples):
        # Concatenate input and target with special tokens
        texts = []
        for input_text, target_text in zip(examples["input"], examples["target"]):
            text = f"{input_text}\\n{target_text}<|endoftext|>"
            texts.append(text)'''
    
    new_tokenize = '''    def tokenize_function(examples):
        # Extract from messages format: user -> assistant conversation
        texts = []
        for messages in examples["messages"]:
            user_msg = messages[0]["content"]  # user message
            assistant_msg = messages[1]["content"]  # assistant response
            text = f"{user_msg}\\n{assistant_msg}<|endoftext|>"
            texts.append(text)'''
    
    # Make the replacement
    content = content.replace(old_tokenize, new_tokenize)
    
    # Write back
    with open("train_v9g_curriculum_fixed.py", "w") as f:
        f.write(content)
    
    print("✅ Created fixed training script: train_v9g_curriculum_fixed.py")
    print("🔧 Tokenization function updated to work with messages format")

if __name__ == "__main__":
    fix_tokenize_function()