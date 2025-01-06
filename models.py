from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PoseAnalysis:
    knee_angle: float
    hip_angle: float
    back_angle: float
    symmetry_score: float
    depth_score: float

@dataclass
class FormClassification:
    is_good: bool
    confidence: float
    feedback: List[str]
    joint_positions: Dict[str, List[float]]
