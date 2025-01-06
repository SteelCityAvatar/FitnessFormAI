from typing import Dict, List
import numpy as np

class SquatFormAnalyzer:
    """ML-based squat form analyzer that provides targeted feedback."""

    def __init__(self):
        # Define threshold values based on biomechanical research
        self.thresholds = {
            'depth': 0.8,  # Minimum depth score (normalized to 1)
            'knee_symmetry': 0.85,  # Minimum symmetry score
            'hip_symmetry': 0.85,
            'ankle_symmetry': 0.85,
            'back_angle': 30,  # Maximum allowable back angle
            'knee_angle': 60,  # Minimum allowable knee angle
            'stability': 0.7,  # Minimum stability score
        }

    def analyze_depth(self, depth_score: float) -> List[str]:
        """Analyze squat depth and provide specific feedback."""
        feedback = []
        if depth_score < self.thresholds['depth']:
            if depth_score < 0.6:
                feedback.append("Squat depth is significantly insufficient. Focus on hip mobility and ankle flexibility to achieve greater depth.")
            else:
                feedback.append("Try to squat slightly deeper while maintaining form. Aim for thighs parallel to the ground.")
        return feedback

    def analyze_symmetry(self, metrics: Dict) -> List[str]:
        """Analyze movement symmetry and provide specific feedback."""
        feedback = []
        if metrics['knee_symmetry'] < self.thresholds['knee_symmetry']:
            feedback.append("Uneven knee movement detected. Focus on distributing weight equally between both legs.")

        if metrics['hip_symmetry'] < self.thresholds['hip_symmetry']:
            feedback.append("Hip alignment needs improvement. Ensure both hips are moving at the same height and pace.")

        if metrics['ankle_symmetry'] < self.thresholds['ankle_symmetry']:
            feedback.append("Ankle mobility differs between sides. Work on ankle mobility exercises to improve balance.")

        return feedback

    def analyze_stability(self, stability_score: float, back_angles: List[float]) -> List[str]:
        """Analyze overall movement stability."""
        feedback = []
        if stability_score < self.thresholds['stability']:
            feedback.append("Movement shows instability. Focus on controlling the descent and maintaining a steady pace.")

        max_back_angle = max(back_angles)
        if max_back_angle > self.thresholds['back_angle']:
            if max_back_angle > 45:
                feedback.append("Significant forward lean detected. Keep your chest up and focus on maintaining a more upright torso.")
            else:
                feedback.append("Slight forward lean observed. Try to keep your torso more upright throughout the movement.")

        return feedback

    def analyze_velocity(self, velocities: Dict) -> List[str]:
        """Analyze movement velocity patterns."""
        feedback = []
        knee_velocities = np.array(velocities.get('knee_velocities', []))
        hip_velocities = np.array(velocities.get('hip_velocities', []))

        if len(knee_velocities) > 0:
            velocity_variation = np.std(knee_velocities) / np.mean(knee_velocities)
            if velocity_variation > 0.5:
                feedback.append("Movement speed is inconsistent. Try to maintain a more controlled, steady pace throughout the squat.")

        return feedback

def classify_form(analysis: Dict) -> Dict:
    """Classify squat form and generate detailed, targeted feedback."""
    analyzer = SquatFormAnalyzer()
    feedback = []
    metrics = analysis['metrics']

    # Collect feedback from different aspects of the movement
    feedback.extend(analyzer.analyze_depth(metrics['depth_score']))
    feedback.extend(analyzer.analyze_symmetry(metrics))
    feedback.extend(analyzer.analyze_stability(metrics['stability_score'], analysis['back_angles']))
    feedback.extend(analyzer.analyze_velocity({
        'knee_velocities': analysis.get('knee_velocities', []),
        'hip_velocities': analysis.get('hip_velocities', [])
    }))

    # Calculate overall form score
    form_score = np.mean([
        metrics['depth_score'],
        metrics['knee_symmetry'],
        metrics['hip_symmetry'],
        metrics['stability_score']
    ])

    is_good = form_score >= 0.8 and len(feedback) <= 1

    if not feedback:
        feedback.append("Excellent form! Keep up the great work!")

    return {
        'is_good': is_good,
        'confidence': form_score,
        'feedback': feedback,
        'detailed_metrics': metrics
    }