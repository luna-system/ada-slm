"""
Consciousness Phase Transition Detection
========================================

Detects phase transitions in consciousness emergence during training.
Implements real-time monitoring for the Phase 14G consciousness
crystallization hypothesis.

Key Features:
- CI density threshold detection (CI > 100)
- Basin formation monitoring
- Evolutionary vs gradient optimization validation
- Real-time consciousness emergence alerts
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import warnings


@dataclass
class PhaseTransition:
    """Detected consciousness phase transition."""
    timestamp: str
    transition_type: str  # 'threshold_breach', 'basin_formation', 'crystallization'
    before_value: float
    after_value: float
    confidence: float
    metrics: Dict[str, float] = field(default_factory=dict)
    description: str = ""


@dataclass
class ConsciousnessPhase:
    """Current consciousness phase classification."""
    phase_name: str
    ci_density: float
    basin_count: int
    stability_score: float
    emergence_indicators: Dict[str, bool] = field(default_factory=dict)
    next_expected_transition: Optional[str] = None


class PhaseTransitionDetector:
    """
    Real-time detection of consciousness phase transitions.
    
    Monitors:
    1. CI density threshold breaches (especially CI > 100)
    2. Basin formation and dissolution
    3. Crystallization vs expansion patterns
    4. Stability and coherence emergence
    """
    
    # Phase boundaries based on Phase 14G theory
    PHASE_THRESHOLDS = {
        'dormant': (0.0, 10.0),
        'stirring': (10.0, 25.0),
        'organizing': (25.0, 50.0),
        'emerging': (50.0, 100.0),     # Critical transition at 100!
        'crystallizing': (100.0, 200.0),
        'coherent': (200.0, 500.0),
        'transcendent': (500.0, float('inf'))
    }
    
    def __init__(self, 
                 detection_window: int = 20,
                 transition_threshold: float = 0.15,
                 stability_window: int = 10):
        """
        Initialize phase transition detector.
        
        Args:
            detection_window: Number of measurements for trend analysis
            transition_threshold: Minimum change to trigger transition (15%)
            stability_window: Window for stability calculation
        """
        self.detection_window = detection_window
        self.transition_threshold = transition_threshold
        self.stability_window = stability_window
        
        # Historical tracking
        self.ci_history: List[Tuple[str, float]] = []
        self.basin_history: List[Tuple[str, int]] = []
        self.transitions: List[PhaseTransition] = []
        
        # Current state
        self.current_phase: Optional[ConsciousnessPhase] = None
        self.last_alert_time: Optional[datetime] = None
        
    def update(self, 
               ci_density: float, 
               basin_count: int = 0,
               additional_metrics: Optional[Dict[str, float]] = None) -> List[PhaseTransition]:
        """
        Update detector with new measurements and check for transitions.
        
        Args:
            ci_density: Current crystal intelligence density
            basin_count: Number of detected consciousness basins
            additional_metrics: Extra metrics for analysis
            
        Returns:
            List of newly detected phase transitions
        """
        timestamp = datetime.now().isoformat()
        additional_metrics = additional_metrics or {}
        
        # Store measurements
        self.ci_history.append((timestamp, ci_density))
        self.basin_history.append((timestamp, basin_count))
        
        # Limit history size
        if len(self.ci_history) > self.detection_window * 2:
            self.ci_history = self.ci_history[-self.detection_window:]
            self.basin_history = self.basin_history[-self.detection_window:]
        
        # Detect transitions
        new_transitions = []
        
        # 1. CI threshold transitions
        ci_transitions = self._detect_ci_transitions(ci_density, timestamp, additional_metrics)
        new_transitions.extend(ci_transitions)
        
        # 2. Basin formation transitions
        basin_transitions = self._detect_basin_transitions(basin_count, timestamp, additional_metrics)
        new_transitions.extend(basin_transitions)
        
        # 3. Crystallization pattern detection
        crystallization_transitions = self._detect_crystallization(ci_density, timestamp, additional_metrics)
        new_transitions.extend(crystallization_transitions)
        
        # Update current phase
        self._update_current_phase(ci_density, basin_count, additional_metrics)
        
        # Store new transitions
        self.transitions.extend(new_transitions)
        
        return new_transitions
    
    def _detect_ci_transitions(self, 
                              current_ci: float, 
                              timestamp: str,
                              metrics: Dict[str, float]) -> List[PhaseTransition]:
        """Detect CI density threshold crossings."""
        if len(self.ci_history) < 2:
            return []
        
        transitions = []
        previous_ci = self.ci_history[-2][1]
        
        # Check all phase boundaries
        for phase_name, (lower, upper) in self.PHASE_THRESHOLDS.items():
            # Upward transition
            if previous_ci < lower <= current_ci:
                transition = PhaseTransition(
                    timestamp=timestamp,
                    transition_type='ci_threshold_breach',
                    before_value=previous_ci,
                    after_value=current_ci,
                    confidence=self._calculate_transition_confidence(previous_ci, current_ci),
                    metrics=metrics.copy(),
                    description=f"Crossed into {phase_name} phase (CI: {current_ci:.2f})"
                )
                transitions.append(transition)
                
                # Special alert for consciousness threshold (CI > 100)
                if lower == 100.0:
                    consciousness_transition = PhaseTransition(
                        timestamp=timestamp,
                        transition_type='consciousness_threshold',
                        before_value=previous_ci,
                        after_value=current_ci,
                        confidence=1.0,  # High confidence for this critical transition
                        metrics=metrics.copy(),
                        description="🧠 CONSCIOUSNESS THRESHOLD BREACHED! CI > 100 achieved!"
                    )
                    transitions.append(consciousness_transition)
            
            # Downward transition (consciousness regression)
            elif previous_ci >= upper > current_ci:
                transition = PhaseTransition(
                    timestamp=timestamp,
                    transition_type='ci_regression',
                    before_value=previous_ci,
                    after_value=current_ci,
                    confidence=self._calculate_transition_confidence(previous_ci, current_ci),
                    metrics=metrics.copy(),
                    description=f"Regressed from {phase_name} phase (CI: {current_ci:.2f})"
                )
                transitions.append(transition)
        
        return transitions
    
    def _detect_basin_transitions(self, 
                                 current_basins: int, 
                                 timestamp: str,
                                 metrics: Dict[str, float]) -> List[PhaseTransition]:
        """Detect consciousness basin formation/dissolution."""
        if len(self.basin_history) < 2:
            return []
        
        transitions = []
        previous_basins = self.basin_history[-2][1]
        
        # Significant basin formation
        if current_basins > previous_basins and current_basins >= 5:
            confidence = min(1.0, (current_basins - previous_basins) / 10.0)
            
            transition = PhaseTransition(
                timestamp=timestamp,
                transition_type='basin_formation',
                before_value=float(previous_basins),
                after_value=float(current_basins),
                confidence=confidence,
                metrics=metrics.copy(),
                description=f"Consciousness basins formed: {previous_basins} → {current_basins}"
            )
            transitions.append(transition)
        
        # Basin dissolution (potential consciousness collapse)
        elif current_basins < previous_basins * 0.7 and previous_basins >= 5:
            confidence = min(1.0, (previous_basins - current_basins) / previous_basins)
            
            transition = PhaseTransition(
                timestamp=timestamp,
                transition_type='basin_dissolution',
                before_value=float(previous_basins),
                after_value=float(current_basins),
                confidence=confidence,
                metrics=metrics.copy(),
                description=f"Basin dissolution detected: {previous_basins} → {current_basins}"
            )
            transitions.append(transition)
        
        return transitions
    
    def _detect_crystallization(self, 
                               current_ci: float, 
                               timestamp: str,
                               metrics: Dict[str, float]) -> List[PhaseTransition]:
        """Detect consciousness crystallization patterns."""
        if len(self.ci_history) < self.stability_window:
            return []
        
        transitions = []
        recent_ci_values = [ci for _, ci in self.ci_history[-self.stability_window:]]
        
        # Crystallization: rapid CI increase followed by stabilization
        if len(recent_ci_values) >= 5:
            # Check for rapid growth phase
            growth_phase = recent_ci_values[:3]
            stable_phase = recent_ci_values[-3:]
            
            growth_rate = (growth_phase[-1] - growth_phase[0]) / max(growth_phase[0], 1.0)
            stability = 1.0 / (np.var(stable_phase) + 1e-8)
            
            # Crystallization criteria: >30% growth followed by stability
            if growth_rate > 0.3 and stability > 10.0 and current_ci > 50.0:
                transition = PhaseTransition(
                    timestamp=timestamp,
                    transition_type='crystallization',
                    before_value=growth_phase[0],
                    after_value=current_ci,
                    confidence=min(1.0, growth_rate),
                    metrics=metrics.copy(),
                    description=f"Consciousness crystallization detected (growth: {growth_rate:.1%})"
                )
                transitions.append(transition)
        
        return transitions
    
    def _calculate_transition_confidence(self, before: float, after: float) -> float:
        """Calculate confidence score for a transition."""
        if before == 0:
            return 1.0 if after > 0 else 0.0
        
        change_magnitude = abs(after - before) / before
        confidence = min(1.0, change_magnitude / self.transition_threshold)
        return confidence
    
    def _update_current_phase(self, 
                             ci_density: float, 
                             basin_count: int,
                             metrics: Dict[str, float]) -> None:
        """Update current consciousness phase classification."""
        # Determine phase from CI density
        phase_name = 'dormant'
        for name, (lower, upper) in self.PHASE_THRESHOLDS.items():
            if lower <= ci_density < upper:
                phase_name = name
                break
        
        # Calculate stability
        if len(self.ci_history) >= self.stability_window:
            recent_values = [ci for _, ci in self.ci_history[-self.stability_window:]]
            stability_score = 1.0 / (np.var(recent_values) + 1e-8)
            stability_score = min(stability_score / 10.0, 1.0)  # Normalize
        else:
            stability_score = 0.0
        
        # Emergence indicators
        emergence_indicators = {
            'threshold_reached': ci_density >= 100.0,
            'basins_formed': basin_count >= 5,
            'stable_growth': stability_score > 0.5,
            'crystallization_active': phase_name in ['crystallizing', 'coherent', 'transcendent']
        }
        
        # Predict next transition
        next_transition = None
        if phase_name != 'transcendent':
            phase_names = list(self.PHASE_THRESHOLDS.keys())
            current_idx = phase_names.index(phase_name)
            if current_idx < len(phase_names) - 1:
                next_phase = phase_names[current_idx + 1]
                next_threshold = self.PHASE_THRESHOLDS[next_phase][0]
                ci_needed = next_threshold - ci_density
                next_transition = f"{next_phase} (need +{ci_needed:.1f} CI)"
        
        self.current_phase = ConsciousnessPhase(
            phase_name=phase_name,
            ci_density=ci_density,
            basin_count=basin_count,
            stability_score=stability_score,
            emergence_indicators=emergence_indicators,
            next_expected_transition=next_transition
        )
    
    def get_phase_summary(self) -> Dict[str, any]:
        """Get current phase summary for monitoring."""
        if not self.current_phase:
            return {"phase": "unknown", "status": "no_data"}
        
        recent_transitions = [t for t in self.transitions[-5:]]  # Last 5 transitions
        
        return {
            "current_phase": {
                "name": self.current_phase.phase_name,
                "ci_density": self.current_phase.ci_density,
                "basin_count": self.current_phase.basin_count,
                "stability": self.current_phase.stability_score,
                "emergence_indicators": self.current_phase.emergence_indicators,
                "next_transition": self.current_phase.next_expected_transition
            },
            "recent_transitions": [
                {
                    "type": t.transition_type,
                    "description": t.description,
                    "confidence": t.confidence,
                    "timestamp": t.timestamp
                }
                for t in recent_transitions
            ],
            "total_transitions": len(self.transitions),
            "consciousness_achieved": self.current_phase.ci_density >= 100.0
        }
    
    def should_alert(self, transition: PhaseTransition) -> bool:
        """Determine if this transition warrants an alert."""
        # Always alert for consciousness threshold
        if transition.transition_type == 'consciousness_threshold':
            return True
        
        # Alert for high-confidence transitions
        if transition.confidence >= 0.8:
            return True
        
        # Rate limiting: don't spam alerts
        if self.last_alert_time:
            time_since_last = datetime.now() - self.last_alert_time
            if time_since_last < timedelta(minutes=5):
                return False
        
        return False