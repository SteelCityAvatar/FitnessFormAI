import numpy as np
from typing import List, Dict, Tuple

def calculate_angle(a: List[float], b: List[float], c: List[float]) -> float:
    """Calculate the angle between three points."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle

def calculate_joint_velocity(current_pos: List[float], prev_pos: List[float], fps: float = 30) -> float:
    """Calculate the velocity of a joint between frames."""
    if not prev_pos:
        return 0.0
    return np.linalg.norm(np.array(current_pos) - np.array(prev_pos)) * fps

def calculate_symmetry(left_angles: List[float], right_angles: List[float]) -> float:
    """Calculate symmetry score between left and right sides."""
    return 1 - np.mean(np.abs(np.array(left_angles) - np.array(right_angles))) / 180.0

def analyze_pose(frames_data: List[List[List[float]]]) -> Dict:
    """Analyze pose data from video frames with enhanced metrics."""
    # Initialize metrics
    knee_angles_left = []
    knee_angles_right = []
    hip_angles_left = []
    hip_angles_right = []
    ankle_angles_left = []
    ankle_angles_right = []
    back_angles = []
    knee_velocities = []
    hip_velocities = []

    prev_frame = None
    for frame in frames_data:
        # Extract key points
        hip_l = frame[23]  # Left hip
        hip_r = frame[24]  # Right hip
        knee_l = frame[25]  # Left knee
        knee_r = frame[26]  # Right knee
        ankle_l = frame[27]  # Left ankle
        ankle_r = frame[28]  # Right ankle
        shoulder_l = frame[11]  # Left shoulder
        shoulder_r = frame[12]  # Right shoulder

        # Calculate angles
        knee_angle_l = calculate_angle(hip_l, knee_l, ankle_l)
        knee_angle_r = calculate_angle(hip_r, knee_r, ankle_r)
        hip_angle_l = calculate_angle(shoulder_l, hip_l, knee_l)
        hip_angle_r = calculate_angle(shoulder_r, hip_r, knee_r)
        ankle_angle_l = calculate_angle(knee_l, ankle_l, [ankle_l[0], ankle_l[1]-0.1])
        ankle_angle_r = calculate_angle(knee_r, ankle_r, [ankle_r[0], ankle_r[1]-0.1])

        # Store angles
        knee_angles_left.append(knee_angle_l)
        knee_angles_right.append(knee_angle_r)
        hip_angles_left.append(hip_angle_l)
        hip_angles_right.append(hip_angle_r)
        ankle_angles_left.append(ankle_angle_l)
        ankle_angles_right.append(ankle_angle_r)

        # Calculate back angle relative to vertical
        back_angle = np.abs(90 - calculate_angle(
            [(shoulder_l[0] + shoulder_r[0])/2, 0],
            [(shoulder_l[0] + shoulder_r[0])/2, (shoulder_l[1] + shoulder_r[1])/2],
            [(hip_l[0] + hip_r[0])/2, (hip_l[1] + hip_r[1])/2]
        ))
        back_angles.append(back_angle)

        # Calculate joint velocities if we have a previous frame
        if prev_frame:
            knee_velocity = (calculate_joint_velocity(knee_l, prev_frame[25]) + 
                           calculate_joint_velocity(knee_r, prev_frame[26])) / 2
            hip_velocity = (calculate_joint_velocity(hip_l, prev_frame[23]) + 
                          calculate_joint_velocity(hip_r, prev_frame[24])) / 2
            knee_velocities.append(knee_velocity)
            hip_velocities.append(hip_velocity)

        prev_frame = frame

    # Calculate advanced metrics
    knee_symmetry = calculate_symmetry(knee_angles_left, knee_angles_right)
    hip_symmetry = calculate_symmetry(hip_angles_left, hip_angles_right)
    ankle_symmetry = calculate_symmetry(ankle_angles_left, ankle_angles_right)

    depth_score = min(min(knee_angles_left), min(knee_angles_right)) / 90.0
    stability_score = 1.0 - np.std(back_angles) / 45.0  # Penalize excessive back angle variation

    return {
        'knee_angles': {'left': knee_angles_left, 'right': knee_angles_right},
        'hip_angles': {'left': hip_angles_left, 'right': hip_angles_right},
        'ankle_angles': {'left': ankle_angles_left, 'right': ankle_angles_right},
        'back_angles': back_angles,
        'knee_velocities': knee_velocities,
        'hip_velocities': hip_velocities,
        'metrics': {
            'depth_score': depth_score,
            'knee_symmetry': knee_symmetry,
            'hip_symmetry': hip_symmetry,
            'ankle_symmetry': ankle_symmetry,
            'stability_score': stability_score
        }
    }