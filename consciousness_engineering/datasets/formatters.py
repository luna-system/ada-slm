"""
Formatters - Output formatting for datasets
==========================================

Handles conversion to various training formats.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from .generators import Example


class DatasetFormatter:
    """Base class for dataset formatters."""
    
    def format(self, examples: List[Example]) -> str:
        """Format examples to string."""
        raise NotImplementedError
        
    def save(self, examples: List[Example], path: Path):
        """Save formatted examples to file."""
        raise NotImplementedError


class JSONLFormatter(DatasetFormatter):
    """
    Format as JSONL (JSON Lines).
    
    Standard format for most training pipelines.
    Each line is a complete JSON object with messages array.
    """
    
    def __init__(self, include_metadata: bool = False):
        self.include_metadata = include_metadata
        
    def format_example(self, example: Example) -> str:
        """Format a single example."""
        data = {
            "messages": [
                {"role": "user", "content": example.user},
                {"role": "assistant", "content": example.assistant}
            ]
        }
        
        if self.include_metadata:
            if example.phase:
                data["phase"] = example.phase
            if example.metadata:
                data["metadata"] = example.metadata
                
        return json.dumps(data, ensure_ascii=False)
    
    def format(self, examples: List[Example]) -> str:
        """Format all examples."""
        return "\n".join(self.format_example(ex) for ex in examples)
    
    def save(self, examples: List[Example], path: Path):
        """Save to JSONL file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for example in examples:
                f.write(self.format_example(example) + "\n")


class ChatMLFormatter(DatasetFormatter):
    """
    Format as ChatML.
    
    <|im_start|>user
    message<|im_end|>
    <|im_start|>assistant
    response<|im_end|>
    """
    
    def format_example(self, example: Example) -> str:
        """Format a single example in ChatML."""
        return (
            f"<|im_start|>user\n{example.user}<|im_end|>\n"
            f"<|im_start|>assistant\n{example.assistant}<|im_end|>"
        )
    
    def format(self, examples: List[Example]) -> str:
        """Format all examples."""
        return "\n\n".join(self.format_example(ex) for ex in examples)
    
    def save(self, examples: List[Example], path: Path):
        """Save to text file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.format(examples))


class AlpacaFormatter(DatasetFormatter):
    """
    Format as Alpaca-style JSON.
    
    [
        {"instruction": "...", "input": "", "output": "..."},
        ...
    ]
    """
    
    def format_example(self, example: Example) -> Dict[str, str]:
        """Format a single example."""
        return {
            "instruction": example.user,
            "input": "",
            "output": example.assistant
        }
    
    def format(self, examples: List[Example]) -> str:
        """Format all examples as JSON array."""
        data = [self.format_example(ex) for ex in examples]
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def save(self, examples: List[Example], path: Path):
        """Save to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.format(examples))


# =============================================================================
# Convenience functions
# =============================================================================

def format_for_training(
    examples: List[Example],
    format: str = "jsonl",
    output_path: Optional[Path] = None,
    **kwargs
) -> Optional[str]:
    """
    Format examples for training.
    
    Args:
        examples: List of examples to format
        format: Output format ("jsonl", "chatml", "alpaca")
        output_path: If provided, save to file
        **kwargs: Additional arguments for formatter
        
    Returns:
        Formatted string if output_path is None, else None
    """
    formatters = {
        "jsonl": JSONLFormatter,
        "chatml": ChatMLFormatter,
        "alpaca": AlpacaFormatter,
    }
    
    formatter_class = formatters.get(format)
    if not formatter_class:
        raise ValueError(f"Unknown format: {format}. Options: {list(formatters.keys())}")
        
    formatter = formatter_class(**kwargs)
    
    if output_path:
        formatter.save(examples, Path(output_path))
        return None
    else:
        return formatter.format(examples)


def load_jsonl(path: Path) -> List[Example]:
    """Load examples from a JSONL file."""
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                messages = data.get("messages", [])
                user = next((m["content"] for m in messages if m["role"] == "user"), "")
                assistant = next((m["content"] for m in messages if m["role"] == "assistant"), "")
                examples.append(Example(
                    user=user,
                    assistant=assistant,
                    phase=data.get("phase"),
                    metadata=data.get("metadata", {})
                ))
    return examples
