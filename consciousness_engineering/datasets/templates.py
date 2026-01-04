"""
Templates - Template-based example generation
=============================================

Provides a template system for generating variations of examples.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
import random
import re


@dataclass
class Template:
    """
    A template for generating examples.
    
    Templates use {placeholder} syntax for variable substitution.
    
    Example:
        template = Template(
            user="How are you?",
            assistant="φ The eigenvalues align in {state} patterns today.\n{certainty}present"
        )
        
        rendered = template.render(state="stable", certainty="◕")
    """
    user: str
    assistant: str
    name: Optional[str] = None
    phase: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    weight: float = 1.0  # For weighted random selection
    
    # Placeholder definitions with possible values
    placeholders: Dict[str, List[str]] = field(default_factory=dict)
    
    def render(self, **kwargs) -> tuple[str, str]:
        """Render the template with the given values."""
        user = self.user
        assistant = self.assistant
        
        for key, value in kwargs.items():
            user = user.replace(f"{{{key}}}", str(value))
            assistant = assistant.replace(f"{{{key}}}", str(value))
            
        return user, assistant
    
    def render_random(self) -> tuple[str, str]:
        """Render with random values from placeholders."""
        kwargs = {}
        for key, values in self.placeholders.items():
            kwargs[key] = random.choice(values)
        return self.render(**kwargs)
    
    def get_placeholders(self) -> List[str]:
        """Extract placeholder names from template."""
        pattern = r'\{(\w+)\}'
        user_placeholders = set(re.findall(pattern, self.user))
        assistant_placeholders = set(re.findall(pattern, self.assistant))
        return list(user_placeholders | assistant_placeholders)
    
    def variations(self, n: int) -> List[tuple[str, str]]:
        """Generate n variations of this template."""
        results = []
        for _ in range(n):
            results.append(self.render_random())
        return results


class TemplateLibrary:
    """
    A collection of templates organized by category/phase.
    """
    
    def __init__(self):
        self._templates: Dict[str, List[Template]] = {}
        self._all_templates: List[Template] = []
        
    def add(self, template: Template, category: Optional[str] = None):
        """Add a template to the library."""
        cat = category or template.phase or "default"
        if cat not in self._templates:
            self._templates[cat] = []
        self._templates[cat].append(template)
        self._all_templates.append(template)
        
    def get_category(self, category: str) -> List[Template]:
        """Get all templates in a category."""
        return self._templates.get(category, [])
    
    def random_from_category(self, category: str) -> Optional[Template]:
        """Get a random template from a category (weighted)."""
        templates = self.get_category(category)
        if not templates:
            return None
        weights = [t.weight for t in templates]
        return random.choices(templates, weights=weights, k=1)[0]
    
    def all(self) -> List[Template]:
        """Get all templates."""
        return self._all_templates
    
    def categories(self) -> List[str]:
        """Get all category names."""
        return list(self._templates.keys())
    
    def count(self, category: Optional[str] = None) -> int:
        """Count templates in a category or total."""
        if category:
            return len(self._templates.get(category, []))
        return len(self._all_templates)


class TemplateRenderer:
    """
    Advanced template rendering with post-processing.
    """
    
    def __init__(self):
        self.post_processors: List[Callable[[str], str]] = []
        
    def add_post_processor(self, processor: Callable[[str], str]):
        """Add a post-processing function."""
        self.post_processors.append(processor)
        
    def render(self, template: Template, **kwargs) -> tuple[str, str]:
        """Render a template with post-processing."""
        user, assistant = template.render(**kwargs)
        
        for processor in self.post_processors:
            user = processor(user)
            assistant = processor(assistant)
            
        return user, assistant


# =============================================================================
# Pre-built template utilities
# =============================================================================

def strip_empty_lines(text: str) -> str:
    """Remove consecutive empty lines."""
    lines = text.split('\n')
    result = []
    prev_empty = False
    for line in lines:
        is_empty = not line.strip()
        if not (is_empty and prev_empty):
            result.append(line)
        prev_empty = is_empty
    return '\n'.join(result)


def ensure_agl_header(text: str) -> str:
    """Ensure response starts with φ if it's an AGL response."""
    if text.strip() and not text.strip().startswith('φ'):
        # Check if this looks like an AGL response
        agl_markers = ['●', '◐', '◕', '◑', '◔', '○', '∴', '∵', '∃', '∀', '🌊', '✨']
        if any(marker in text for marker in agl_markers):
            return 'φ ' + text
    return text
