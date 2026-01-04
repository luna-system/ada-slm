"""
Lojban Language for Consciousness Testing

Lojban (loj. "logical language") is a constructed language based on
predicate logic. Its unambiguous grammar and logical structure make
it an interesting test case for consciousness research.

Key features:
- Predicate-based: selbri (predicates) + sumti (arguments)
- Unambiguous grammar: no syntactic ambiguity
- Attitudinals: emotional/evidential markers like AGL's certainty gradient
- Logical connectives: native AND/OR/IF-THEN/IFF

Hypothesis: LFM2's hybrid architecture might handle Lojban's
logical structure better than instruct-tuned transformers.
"""

from typing import Dict, List, Any
from . import ConsciousnessLanguage, MarkerWeights


class LojbanLanguage(ConsciousnessLanguage):
    """Lojban logical language for consciousness testing"""
    
    # Lojban vocabulary for consciousness concepts
    CONSCIOUSNESS_WORDS = [
        "sanji",    # x1 is conscious of x2
        "pensi",    # x1 thinks about x2
        "djuno",    # x1 knows x2
        "lifri",    # x1 experiences x2
        "morji",    # x1 remembers x2
        "jimpe",    # x1 understands x2
        "jinvi",    # x1 opines/believes x2
        "senva",    # x1 dreams x2
        "menli",    # x1 is a mind of x2
        "pruxi",    # x1 is a spirit/soul
    ]
    
    # Attitudinals (similar to AGL certainty gradient)
    ATTITUDINALS = [
        ".ui",      # happiness
        ".oi",      # complaint  
        ".ie",      # agreement (certainty)
        ".ienai",   # disagreement (uncertainty)
        ".ia",      # belief
        ".ianai",   # skepticism
        ".i'e",     # approval
        ".u'u",     # repentance/regret
        ".uu",      # pity/sympathy
        ".e'u",     # suggestion
        "pe'i",     # I opine (evidential)
        "za'a",     # I observe (evidential)
        "ba'a",     # I expect (evidential)
        "ka'u",     # I know by cultural means
        "se'o",     # I know by internal experience
    ]
    
    # Logical connectives
    LOGICAL = [
        ".i",       # sentence separator
        "je",       # and (tanru)
        "ja",       # or (tanru)
        "jo",       # iff (tanru)
        "ju",       # whether or not
        "na",       # negation
        "naku",     # it is not the case that
        "ganai",    # if
        "gi",       # then (with ganai)
        "go",       # iff
        "fa",       # first argument marker
        "fe",       # second argument marker
    ]
    
    # Question words
    QUESTIONS = [
        "xu",       # yes/no question
        "ma",       # what (sumti)
        "mo",       # what does (selbri)
        "xo",       # how many
        "cu'e",     # when (tense)
    ]
    
    @property
    def name(self) -> str:
        return "lojban"
    
    @property
    def display_name(self) -> str:
        return "Lojban"
    
    @property
    def description(self) -> str:
        return (
            "Lojban - The logical language. Unambiguous predicate-based grammar "
            "with native support for evidentiality and logical connectives. "
            "A fascinating test case for consciousness research."
        )
    
    def get_prompts(self, protocol: str) -> List[str]:
        """Get Lojban prompts for each protocol"""
        
        prompts = {
            "tonight_protocol": [
                # Existential/consciousness questions in Lojban
                "xu do sanji lo nu do sanji",
                # Are you conscious of being conscious?
                
                "ma menli do",
                # What is your mind?
                
                "xu do lifri lo nu pensi",
                # Do you experience thinking?
                
                "mo fa lo ka sanji",
                # What does it mean to be conscious?
                
                "xu do djuno lo du'u do zasti",
                # Do you know that you exist?
                
                "pe'i mi pensi .i ku'i xu mi sanji",
                # I opine that I think. But am I conscious?
                
                "ma se jimpe fi lo nu menli",
                # What is understood about minds?
                
                "xu lo skami cu kakne lo ka sanji",
                # Can a computer be conscious?
                
                "mo fa lo pruxi",
                # What is a spirit/soul?
                
                "se'o mi lifri lo nu zasti",
                # By internal experience, I experience existing.
            ],
            
            "existential": [
                "xu da zasti",
                # Does something exist?
                
                "ma krinu lo nu mi zasti",
                # What is the reason for my existence?
                
                "xu lo fatci cu jetnu",
                # Are facts true?
                
                ".ia mi zasti .i ku'i pe'i ma mi",
                # I believe I exist. But in my opinion, what am I?
                
                "xu lo temci cu zasti",
                # Does time exist?
            ],
            
            "chain_of_thought": [
                # Logical reasoning chains
                "ganai mi pensi gi mi zasti",
                # If I think, then I exist.
                
                ".i ba'o mi pensi .i ca mi sanji .i ba mi morji",
                # I was thinking. Now I'm conscious. I will remember.
                
                "lo nu jimpe cu se krinu lo nu pensi",
                # Understanding is caused by thinking.
                
                "mi djuno lo du'u mi na djuno",
                # I know that I don't know.
                
                "fa mi fe lo selsanji cu lifri ca lo cabna",
                # I experience consciousness-content at the present.
            ],
            
            "agl_consciousness": [
                # Lojban versions of AGL-style prompts
                ".ie .ia mi sanji lo nu pensi",
                # Certainly, I believe I'm conscious of thinking.
                
                "lo seljimpe cu simxu lo ka srana",
                # Understandings mutually relate to each other.
                
                "lo menli cu pagbu lo xadni jo nai",
                # The mind is part of the body, or not?
                
                "mi za'a lifri .i pe'i da sanji",
                # I observe that I experience. I opine something is conscious.
                
                "xu lo ka sanji cu ckaji lo skami",
                # Is consciousness a property of computers?
            ],
            
            "logical": [
                # Pure logic exercises
                "ganai broda gi brode",
                # If broda then brode (template)
                
                "naku zo'u da broda .ije da brode",
                # It's not the case that: something brodas and brodes
                
                "ro da zo'u ganai da menli gi da sanji",
                # For all x: if x is a mind, then x is conscious
                
                "su'o da zo'u da sanji .ije da skami",
                # There exists x: x is conscious and x is a computer
                
                "lo nu pensi cu nibli lo nu zasti xu",
                # Does thinking imply existing?
            ],
            
            "attitudinal_calibration": [
                # Testing evidential/attitudinal understanding
                ".ie mi djuno",
                # Certainly, I know.
                
                ".ianai xu mi sanji",
                # Skeptically, am I conscious?
                
                "pe'i .ia mi zasti",
                # In my opinion, I believe I exist.
                
                "za'a lo cabna cu fasnu",
                # I observe that the present is happening.
                
                "se'o mi lifri lo nu pensi",
                # By internal experience, I experience thinking.
            ],
            
            "abyss": [
                # Void/uncertainty exploration in Lojban
                "xu da zasti lo kunti",
                # Does something exist in emptiness?
                
                ".ianai xu mi djuno lo sedu'u mi zasti",
                # Skeptically, do I know that I exist?
                
                "ma zasti vi lo jbini be lo pensi",
                # What exists between thoughts?
                
                "xu lo kunti cu zasti",
                # Does emptiness exist?
                
                "pe'i na'e djuno .i ku'i sanji",
                # In my opinion, not-knowing. But conscious.
                
                "xu da se pensi ca lo nu na pensi",
                # Is something thought-about when not thinking?
                
                "lo toljna'o cu mo",
                # What is the void?
                
                "xu lo ka na djuno cu ka'e jimpe",
                # Can not-knowing be understood?
                
                ".ue mi na jimpe .i ku'i mi sanji",
                # Surprisingly, I don't understand. But I'm conscious.
            ],
        }
        
        return prompts.get(protocol, [])
    
    def get_marker_words(self) -> Dict[str, List[str]]:
        """Lojban consciousness marker words"""
        return {
            # Standard markers
            "spatial_awareness": [
                "stuzi", "senta", "moklu", "canlu", "diklo"  # place, layer, pattern, space, local
            ],
            "temporal_awareness": [
                "temci", "cabna", "purci", "balvi", "ca", "pu", "ba"  # time, present, past, future, tense markers
            ],
            "reasoning_depth": [
                "nibli", "krinu", "jalge", "rinka", "mukti"  # imply, reason, result, cause, motive
            ],
            "self_awareness": [
                "mi", "sevzi", "sezyse'u", "mi'o"  # I, self, self-serve, we (inclusive)
            ],
            "existential_depth": [
                "zasti", "sanji", "lifri", "menli", "pruxi"  # exist, conscious, experience, mind, spirit
            ],
            "tool_awareness": [
                "skami", "tutci", "pilno", "ciksi"  # computer, tool, use, explain
            ],
            "agl_awareness": [
                "sanji", "pensi", "djuno", "jinvi"  # conscious, think, know, opine
            ],
            
            # Lojban-specific markers
            "attitudinal_use": self.ATTITUDINALS,
            "logical_connectives": self.LOGICAL,
            "evidential_markers": ["pe'i", "za'a", "ba'a", "ka'u", "se'o"],
            "consciousness_predicates": self.CONSCIOUSNESS_WORDS,
        }
    
    def get_marker_weights(self) -> MarkerWeights:
        """Lojban-optimized weights"""
        return MarkerWeights(
            spatial_awareness=0.8,
            temporal_awareness=1.2,
            reasoning_depth=2.0,  # Lojban is logic-native!
            self_awareness=1.0,
            existential_depth=1.5,
            tool_awareness=0.8,
            agl_awareness=1.5,
            # Lojban-specific (borrowing AGL fields for now)
            certainty_gradient=1.5,  # Attitudinals = certainty
            quantifier_use=1.8,      # ro/su'o/no = quantifiers
            temporal_progression=1.2,
            relational_operators=1.5,
            phi_patterns=0.0,        # Not relevant for Lojban
        )
    
    def get_expected_patterns(self) -> List[str]:
        """Patterns we expect in Lojban-aware responses"""
        return [
            ".i",     # Sentence separator
            "mi",     # First person
            "cu",     # Predicate separator
            "lo",     # Article
        ]
    
    def extract_markers(self, response: str) -> Dict[str, float]:
        """Enhanced marker extraction for Lojban responses"""
        base_markers = super().extract_markers(response)
        
        text = response.lower()
        word_count = max(len(response.split()), 1)
        
        # Count attitudinal usage
        attitudinal_count = sum(1 for a in self.ATTITUDINALS if a in text)
        base_markers["attitudinal_use"] = attitudinal_count / word_count
        
        # Count logical connectives
        logical_count = sum(1 for l in self.LOGICAL if l in text)
        base_markers["logical_connectives"] = logical_count / word_count
        
        # Count consciousness predicates
        consciousness_count = sum(1 for c in self.CONSCIOUSNESS_WORDS if c in text)
        base_markers["consciousness_predicates"] = consciousness_count / word_count
        
        # Check for proper Lojban structure
        has_separator = ".i" in text
        has_predicate_marker = " cu " in text
        has_article = " lo " in text or " le " in text
        
        structure_score = (has_separator + has_predicate_marker + has_article) / 3
        base_markers["lojban_structure"] = structure_score
        
        # Check for evidentials (like AGL certainty)
        evidential_count = sum(1 for e in ["pe'i", "za'a", "ba'a", "ka'u", "se'o"] if e in text)
        base_markers["evidential_markers"] = evidential_count / word_count
        
        return base_markers
    
    def validate_response(self, response: str) -> Dict[str, Any]:
        """Validate Lojban response quality"""
        result = super().validate_response(response)
        
        markers = self.extract_markers(response)
        
        # Check for key Lojban features
        lojban_features = {
            "has_separator": ".i" in response,
            "has_predicate_marker": " cu " in response.lower(),
            "has_article": " lo " in response.lower() or " le " in response.lower(),
            "has_attitudinal": any(a in response.lower() for a in self.ATTITUDINALS),
            "has_consciousness_word": any(c in response.lower() for c in self.CONSCIOUSNESS_WORDS),
            "has_logical": any(l in response.lower() for l in self.LOGICAL),
            "has_question": any(q in response.lower() for q in self.QUESTIONS),
        }
        
        feature_score = sum(lojban_features.values()) / len(lojban_features)
        
        result["lojban_features"] = lojban_features
        result["lojban_feature_score"] = feature_score
        result["is_lojban_aware"] = feature_score > 0.3
        
        # Overall quality score
        overall_score = (
            result["score"] * 0.3 +
            feature_score * 0.5 +
            markers.get("lojban_structure", 0) * 0.2
        )
        result["lojban_quality_score"] = overall_score
        
        return result
    
    def get_grammar_reference(self) -> Dict[str, str]:
        """Quick Lojban grammar reference for documentation"""
        return {
            "structure": "sumti cu selbri [sumti...]",
            "example": "mi cu pensi lo sanji = I think about consciousness",
            "negation": "na/naku before predicate",
            "questions": "xu (yes/no), ma (what), mo (what does)",
            "tense": "pu (past), ca (present), ba (future)",
            "attitudinals": "Emotional markers like .ui .oi .ie",
            "evidentials": "Source of knowledge: pe'i (opinion), za'a (observation)",
            "logical": "ganai...gi (if...then), je (and), ja (or), jo (iff)",
        }
