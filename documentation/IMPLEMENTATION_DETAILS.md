# Detailed Implementation Walkthrough

## Core Components

### 1. Video Processing Pipeline
The application processes video input in two ways:
- Live webcam feed via WebSocket
- Uploaded video files via HTTP POST

#### How it works:
```
Video Input -> Frame Extraction -> Pose Detection -> Analysis -> Real-time Feedback
```

### 2. Pose Analysis System
Located in `utils/pose_analyzer.py`, this component:
- Calculates joint angles (knees, hips, back)
- Measures movement symmetry
- Tracks depth and stability
- Computes velocity patterns

Key metrics tracked:
- Knee angles (left/right)
- Hip angles (left/right)
- Back angle relative to vertical
- Movement symmetry scores
- Squat depth percentage
- Stability score

### 3. Form Classification
Found in `utils/classifier.py`, this system:
- Analyzes multiple aspects of the squat
- Generates targeted feedback
- Provides confidence scores
- Uses biomechanical thresholds

Feedback categories:
- Depth recommendations
- Symmetry improvements
- Stability suggestions
- Velocity adjustments

### 4. Frontend Interface
The user interface (`templates/index.html` and associated JS files) provides:
- Live video preview
- Real-time feedback display
- Form analysis graphs
- File upload capability

## Technical Implementation Details

### WebSocket Communication
- Uses Flask-SocketIO for real-time data transfer
- Handles frame-by-frame processing
- Manages bi-directional communication

### MediaPipe Integration
- Uses CPU-only mode for compatibility
- Extracts 33 body landmarks
- Provides 3D coordinates for joint calculations

### Data Flow
1. Video Input Processing:
   - Frame capture (webcam or file)
   - Conversion to RGB format
   - Landmark detection

2. Analysis Pipeline:
   - Joint angle calculations
   - Metric computation
   - Form classification
   - Feedback generation

3. Frontend Updates:
   - Real-time pose visualization
   - Metric graphs
   - Feedback display

## Current Features

### Implemented
- Real-time pose detection
- Comprehensive form analysis
- Detailed feedback generation
- Video upload processing
- Live webcam analysis
- Interactive UI

### In Progress
- Performance optimizations
- Additional exercise support
- Enhanced visualization

## File Structure Explanation

### Backend Files
- `app.py`: Main application logic and WebSocket handlers
- `main.py`: Server initialization and configuration
- `models.py`: Data structure definitions

### Analysis Components
- `utils/pose_analyzer.py`: Core analysis algorithms
- `utils/classifier.py`: Form classification and feedback

### Frontend Components
- `templates/index.html`: Main UI template
- `static/js/app.js`: Client-side logic
- `static/js/canvas.js`: Visualization rendering
- `static/css/style.css`: Custom styling

## Development Decisions

### Why Flask & WebSocket?
- Real-time communication needed for live analysis
- Simple yet powerful web framework
- Easy integration with Python ML tools

### Why MediaPipe?
- Robust pose detection
- CPU-only capability
- Real-time processing performance

### Why Bootstrap Dark Theme?
- Professional appearance
- Built-in responsive design
- Consistent user experience
