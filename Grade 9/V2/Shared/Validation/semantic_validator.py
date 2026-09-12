"""
Strict Visual Semantic Validator.
Defends against PR #310 bypassing (where graphics are hardcoded but claim to be data-grounded).
"""
from typing import Any, Dict, List
import re

class VisualSemanticValidator:
    """
    Validates that a generated graphic physically contains the semantic
    values requested by the engine parameters.
    """

    @staticmethod
    def extract_numeric_tokens(text: str) -> List[str]:
        """Extract all numeric sequences from a string."""
        return re.findall(r'\d+', str(text))
    
    @staticmethod
    def extract_word_tokens(text: str) -> List[str]:
        """Extract alphabetic words (case-insensitive)."""
        return re.findall(r'[A-Za-z]+', str(text).lower())

    @staticmethod
    def validate_evidence(evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates a single piece of evidence from a render backend.
        Requires evidence to have 'params' and 'rendered_evidence.labels'.
        """
        params = evidence.get("params", {})
        rendered = evidence.get("rendered_evidence", {})
        labels = rendered.get("labels", [])
        
        if not labels:
            return {"pass": False, "reason": "No labels rendered", "missing": list(params.keys())}
        
        all_labels_text = " ".join([str(l) for l in labels])
        rendered_nums = VisualSemanticValidator.extract_numeric_tokens(all_labels_text)
        rendered_words = VisualSemanticValidator.extract_word_tokens(all_labels_text)
        
        missing_params = []
        
        # Traverse params to ensure every meaningful primitive parameter is visually grounded
        for k, v in params.items():
            # Skip metadata keys
            if k in ["tier", "actor", "meaning", "action", "context"]:
                continue
                
            if isinstance(v, (int, float)):
                v_str = str(v)
                # If it's a decimal, check if it exists in the raw text directly
                if '.' in v_str:
                    if v_str not in all_labels_text:
                        missing_params.append(f"{k}={v_str}")
                else:
                    if v_str not in rendered_nums:
                        missing_params.append(f"{k}={v_str}")
                        
            elif isinstance(v, str):
                # For strings, if they are numeric
                if v.isdigit() and v not in rendered_nums:
                    missing_params.append(f"{k}={v}")
                elif not v.isdigit():
                    # Check if at least some significant words match
                    words = VisualSemanticValidator.extract_word_tokens(v)
                    # For long strings, just require one significant token to map (e.g. category names)
                    if words:
                        if not any(w in rendered_words for w in words):
                            missing_params.append(f"{k}={v}")
                            
            elif isinstance(v, list):
                # Flatten simple lists (like categories or values)
                for item in v:
                    if isinstance(item, (int, float)):
                        i_str = str(item)
                        if '.' in i_str:
                            if i_str not in all_labels_text:
                                missing_params.append(f"{k} item {i_str}")
                        else:
                            if i_str not in rendered_nums:
                                missing_params.append(f"{k} item {i_str}")
                    elif isinstance(item, str):
                        words = VisualSemanticValidator.extract_word_tokens(item)
                        if words and not any(w in rendered_words for w in words):
                            missing_params.append(f"{k} item {item}")
        
        if missing_params:
            return {
                "pass": False,
                "reason": "Visual Primitive Semantic Mismatch Detected",
                "missing": missing_params
            }
            
        return {"pass": True}
