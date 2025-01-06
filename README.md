# AI-Powered Squat Form Analyzer Documentation

## Project Overview
An advanced computer vision web application that provides real-time AI-powered squat form analysis and personalized fitness feedback. The application uses MediaPipe for pose detection and custom ML models for form analysis.

## Technology Stack
- **Backend**: Flask with WebSocket support (Flask-SocketIO)
- **Computer Vision**: MediaPipe Pose Detection
- **Frontend**: HTML5, JavaScript, Bootstrap Dark Theme
- **Real-time Communication**: Socket.IO
- **Video Processing**: OpenCV (cv2)

## File Structure
```
├── app.py                 # Main Flask application with WebSocket handlers
├── main.py               # Server entry point
├── models.py             # Data models for pose analysis
├── static/
│   ├── css/
│   │   └── style.css    # Custom styling
│   └── js/
│       ├── app.js       # Main frontend application logic
│       └── canvas.js    # Canvas rendering for pose visualization
├── templates/
│   └── index.html       # Main application interface
└── utils/
    ├── classifier.py    # ML-based form classification
    └── pose_analyzer.py # Pose analysis algorithms
```

## Component Details

### 1. Backend Components

#### app.py
- Initializes Flask application and WebSocket server
- Configures MediaPipe Pose detection
- Handles real-time video processing
- Processes uploaded videos
- Manages WebSocket events for live analysis

#### main.py
- Server entry point
- Configures eventlet for WebSocket support
- Sets up logging and error handling

#### models.py
- Defines data structures for pose analysis
- Contains `PoseAnalysis` and `FormClassification` classes

### 2. Analysis Components

#### utils/pose_analyzer.py
- Implements pose analysis algorithms
- Calculates joint angles and movements
- Computes metrics like:
  - Knee angles
  - Hip angles
  - Back angle
  - Movement symmetry
  - Depth score
  - Joint velocities

#### utils/classifier.py
- ML-based squat form analyzer
- Provides targeted feedback
- Analyzes:
  - Movement depth
  - Symmetry
  - Stability
  - Velocity patterns

### 3. Frontend Components

#### templates/index.html
- Responsive web interface
- Live video preview
- Analysis results display
- File upload functionality
- Bootstrap-based dark theme

#### static/js/app.js
- Manages WebSocket connections
- Handles video capture and streaming
- Processes analysis results
- Updates UI elements

#### static/js/canvas.js
- Renders analysis visualizations
- Draws angle graphs
- Displays pose landmarks

#### static/css/style.css
- Custom styling for components
- Dark theme modifications
- Responsive design adjustments

## Key Features

### Real-time Analysis
- Live webcam feed processing
- Instant form feedback
- Visual pose tracking
- Real-time metrics calculation

### Comprehensive Metrics
- Joint angle tracking
- Movement symmetry analysis
- Depth measurement
- Stability scoring
- Velocity analysis

### Form Classification
- ML-based form assessment
- Detailed feedback generation
- Confidence scoring
- Multiple aspect analysis

### User Interface
- Dark theme interface
- Live video preview
- Real-time feedback display
- Interactive visualizations
- File upload support

## Implementation Details

### Pose Detection
- Uses MediaPipe Pose with CPU optimization
- Extracts 33 body landmarks
- Processes frames in real-time
- Handles both live and uploaded videos

### Analysis Pipeline
1. Frame capture/receipt
2. Pose detection
3. Landmark extraction
4. Angle calculations
5. Metrics computation
6. Form classification
7. Feedback generation

### WebSocket Communication
- Bi-directional real-time data flow
- Frame-by-frame analysis
- Instant feedback delivery
- Error handling and recovery

### Visualization
- Real-time pose overlay
- Angle graphs
- Metric visualizations
- Feedback display

## Setup Instructions

### Prerequisites
- Python 3.x
- Required packages:
  - flask-socketio
  - eventlet
  - opencv-python
  - mediapipe
  - numpy

### Installation
1. Install required packages:
```bash
pip install flask-socketio eventlet opencv-python mediapipe numpy
```

2. Start the server:
```bash
python main.py
```

3. Access the application at `http://localhost:5000`

## Current Status
- Core functionality implemented
- Real-time analysis working
- Basic form feedback operational
- Video upload processing complete
- Live mode implementation in progress

## Next Steps
- Enhanced ML model integration
- Additional exercise support
- Detailed form metrics
- Performance optimization
- User experience improvements
